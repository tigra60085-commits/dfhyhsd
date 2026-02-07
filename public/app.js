const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");
const clientIdEl = document.getElementById("client-id");
const ownPublicKeyEl = document.getElementById("own-public-key");
const copyPublicKeyBtn = document.getElementById("copy-public-key");
const contactsEl = document.getElementById("contacts");
const activeContactEl = document.getElementById("active-contact");
const messageEl = document.getElementById("message");
const sendBtn = document.getElementById("send");
const chatEl = document.getElementById("chat");

const state = {
  clientId: null,
  ownKeyPair: null,
  ownPublicKeyPem: null,
  contacts: new Map(),
  activeContactId: null
};

const encoder = new TextEncoder();
const decoder = new TextDecoder();

const api = {
  async generateKeyPair() {
    return crypto.subtle.generateKey(
      {
        name: "ECDH",
        namedCurve: "P-256"
      },
      true,
      ["deriveKey", "deriveBits"]
    );
  },

  async exportPublicKey(key) {
    const spki = await crypto.subtle.exportKey("spki", key);
    return bufferToPem(spki, "PUBLIC KEY");
  },

  async importPublicKey(pem) {
    const buffer = pemToBuffer(pem);
    return crypto.subtle.importKey(
      "spki",
      buffer,
      {
        name: "ECDH",
        namedCurve: "P-256"
      },
      true,
      []
    );
  },

  async deriveSharedKey(privateKey, publicKey) {
    return crypto.subtle.deriveKey(
      {
        name: "ECDH",
        public: publicKey
      },
      privateKey,
      {
        name: "AES-GCM",
        length: 256
      },
      false,
      ["encrypt", "decrypt"]
    );
  },

  async encrypt(sharedKey, data) {
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ciphertext = await crypto.subtle.encrypt(
      {
        name: "AES-GCM",
        iv
      },
      sharedKey,
      encoder.encode(data)
    );
    return {
      iv: bufferToBase64(iv.buffer),
      content: bufferToBase64(ciphertext)
    };
  },

  async decrypt(sharedKey, payload) {
    const iv = base64ToBuffer(payload.iv);
    const content = base64ToBuffer(payload.content);
    const decrypted = await crypto.subtle.decrypt(
      {
        name: "AES-GCM",
        iv: new Uint8Array(iv)
      },
      sharedKey,
      content
    );
    return decoder.decode(decrypted);
  }
};

const bufferToPem = (buffer, label) => {
  const base64 = bufferToBase64(buffer);
  const lines = base64.match(/.{1,64}/g) || [];
  return `-----BEGIN ${label}-----\n${lines.join("\n")}\n-----END ${label}-----`;
};

const pemToBuffer = (pem) => {
  const base64 = pem.replace(/-----(BEGIN|END) PUBLIC KEY-----/g, "").replace(/\s+/g, "");
  return base64ToBuffer(base64);
};

const bufferToBase64 = (buffer) =>
  btoa(String.fromCharCode(...new Uint8Array(buffer)));

const base64ToBuffer = (base64) => {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
};

const renderContacts = () => {
  contactsEl.innerHTML = "";
  if (state.contacts.size === 0) {
    contactsEl.innerHTML = '<p class="muted">Ожидаем подключений...</p>';
    activeContactEl.textContent = "Пока нет подключенных контактов.";
    activeContactEl.classList.add("muted");
    sendBtn.disabled = true;
    return;
  }

  for (const [contactId, contact] of state.contacts.entries()) {
    const card = document.createElement("div");
    card.className = `contact-card${state.activeContactId === contactId ? " active" : ""}`;

    const button = document.createElement("button");
    button.type = "button";
    button.innerHTML = `<strong>${contactId}</strong><p>${contact.publicKeyPem ? "Ключ получен" : "Ожидаем ключ"}</p>`;
    button.addEventListener("click", () => setActiveContact(contactId));

    card.appendChild(button);
    contactsEl.appendChild(card);
  }

  if (!state.activeContactId) {
    setActiveContact(Array.from(state.contacts.keys())[0]);
  }
};

const setActiveContact = (contactId) => {
  state.activeContactId = contactId;
  renderContacts();
  const contact = state.contacts.get(contactId);
  if (!contact) {
    return;
  }
  activeContactEl.classList.remove("muted");
  activeContactEl.innerHTML = `
    <strong>${contactId}</strong>
    <p>Статус ключа: ${contact.publicKeyPem ? "готов" : "ожидаем"}</p>
  `;
  sendBtn.disabled = !contact.publicKeyPem;
};

const addMessage = (text, meta, outgoing = false) => {
  const item = document.createElement("div");
  item.className = `chat__item${outgoing ? " outgoing" : ""}`;
  item.innerHTML = `<div>${text}</div><div class="chat__meta">${meta}</div>`;
  chatEl.appendChild(item);
  chatEl.scrollTop = chatEl.scrollHeight;
};

const updateConnectionStatus = (connected) => {
  statusText.textContent = connected ? "Подключено" : "Отключено";
  statusDot.classList.toggle("online", connected);
  statusDot.classList.toggle("offline", !connected);
};

const ensureContact = (clientId) => {
  if (!state.contacts.has(clientId)) {
    state.contacts.set(clientId, { publicKeyPem: null, sharedKey: null });
  }
};

const connect = async () => {
  updateConnectionStatus(false);
  const ws = new WebSocket(`${location.origin.replace(/^http/, "ws")}`);

  ws.addEventListener("open", () => {
    updateConnectionStatus(true);
  });

  ws.addEventListener("close", () => {
    updateConnectionStatus(false);
  });

  ws.addEventListener("message", async (event) => {
    const payload = JSON.parse(event.data);
    if (payload.type === "welcome") {
      state.clientId = payload.clientId;
      clientIdEl.textContent = state.clientId;
      payload.activeClients.forEach((id) => ensureContact(id));
      renderContacts();
      if (state.ownPublicKeyPem) {
        ws.send(JSON.stringify({ type: "client-public-key", publicKey: state.ownPublicKeyPem }));
      }
      return;
    }

    if (payload.type === "client-joined") {
      ensureContact(payload.clientId);
      renderContacts();
      if (state.ownPublicKeyPem) {
        ws.send(JSON.stringify({ type: "client-public-key", publicKey: state.ownPublicKeyPem }));
      }
      return;
    }

    if (payload.type === "client-left") {
      state.contacts.delete(payload.clientId);
      if (state.activeContactId === payload.clientId) {
        state.activeContactId = null;
      }
      renderContacts();
      return;
    }

    if (payload.type === "client-public-key") {
      ensureContact(payload.clientId);
      const contact = state.contacts.get(payload.clientId);
      contact.publicKeyPem = payload.publicKey;
      contact.sharedKey = await api.deriveSharedKey(state.ownKeyPair.privateKey, await api.importPublicKey(payload.publicKey));
      renderContacts();
      if (state.activeContactId === payload.clientId) {
        sendBtn.disabled = false;
        activeContactEl.innerHTML = `
          <strong>${payload.clientId}</strong>
          <p>Статус ключа: готов</p>
        `;
      }
      return;
    }

    if (payload.type === "encrypted-message") {
      const contact = state.contacts.get(payload.from);
      if (!contact?.sharedKey) {
        addMessage("Не удалось расшифровать сообщение: общий ключ не готов", "ошибка", false);
        return;
      }
      try {
        const decrypted = await api.decrypt(contact.sharedKey, payload.message);
        addMessage(decrypted, `от ${payload.from}`, false);
      } catch (error) {
        addMessage("Не удалось расшифровать сообщение", "ошибка", false);
      }
    }
  });

  sendBtn.addEventListener("click", async () => {
    const text = messageEl.value.trim();
    if (!text || !state.activeContactId) {
      return;
    }
    const contact = state.contacts.get(state.activeContactId);
    if (!contact?.sharedKey) {
      return;
    }
    const encrypted = await api.encrypt(contact.sharedKey, text);
    ws.send(JSON.stringify({ type: "encrypted-message", message: encrypted }));
    addMessage(text, "вы", true);
    messageEl.value = "";
  });

  return ws;
};

const init = async () => {
  state.ownKeyPair = await api.generateKeyPair();
  state.ownPublicKeyPem = await api.exportPublicKey(state.ownKeyPair.publicKey);
  ownPublicKeyEl.value = state.ownPublicKeyPem;

  copyPublicKeyBtn.addEventListener("click", async () => {
    await navigator.clipboard.writeText(state.ownPublicKeyPem);
    copyPublicKeyBtn.textContent = "Скопировано!";
    setTimeout(() => {
      copyPublicKeyBtn.textContent = "Скопировать";
    }, 1500);
  });

  await connect();
};

init().catch((error) => {
  console.error(error);
  updateConnectionStatus(false);
});
