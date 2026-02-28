const path = require("path");
const crypto = require("crypto");
const express = require("express");
const { WebSocketServer } = require("ws");

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, "public")));

const server = app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

const wss = new WebSocketServer({ server });

const clients = new Map();

const broadcast = (data, excludeId) => {
  for (const [clientId, ws] of clients.entries()) {
    if (clientId !== excludeId && ws.readyState === ws.OPEN) {
      ws.send(JSON.stringify(data));
    }
  }
};

wss.on("connection", (ws) => {
  const clientId = crypto.randomUUID();
  clients.set(clientId, ws);

  ws.send(
    JSON.stringify({
      type: "welcome",
      clientId,
      activeClients: Array.from(clients.keys()).filter((id) => id !== clientId)
    })
  );

  broadcast({ type: "client-joined", clientId }, clientId);

  ws.on("message", (message) => {
    let payload;
    try {
      payload = JSON.parse(message);
    } catch (error) {
      ws.send(JSON.stringify({ type: "error", message: "Invalid JSON" }));
      return;
    }

    if (!payload.type) {
      ws.send(JSON.stringify({ type: "error", message: "Missing type" }));
      return;
    }

    switch (payload.type) {
      case "client-public-key":
        broadcast(
          {
            type: "client-public-key",
            clientId,
            publicKey: payload.publicKey
          },
          clientId
        );
        break;
      case "encrypted-message":
        broadcast(
          {
            type: "encrypted-message",
            from: clientId,
            message: payload.message
          },
          clientId
        );
        break;
      default:
        ws.send(JSON.stringify({ type: "error", message: "Unknown type" }));
        break;
    }
  });

  ws.on("close", () => {
    clients.delete(clientId);
    broadcast({ type: "client-left", clientId }, clientId);
  });
});
