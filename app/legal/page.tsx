export default function LegalPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Legal Disclaimer</h1>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="prose max-w-none">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Educational Purpose Only</h2>
              
              <p className="text-gray-700 mb-4">
                All information provided on this website is for educational and scientific purposes only. 
                This content does not constitute medical advice, diagnosis, or treatment recommendations.
              </p>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">No Medical Advice</h3>
              <p className="text-gray-700 mb-4">
                The content on this site is not intended to replace professional medical advice, diagnosis, 
                or treatment. Always seek the advice of your physician or other qualified health provider 
                with any questions you may have regarding a medical condition or treatment.
              </p>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">Regulatory Status</h3>
              <p className="text-gray-700 mb-4">
                Many substances discussed on this website are not approved for human consumption by regulatory 
                authorities such as the FDA, EMA, or other national agencies. Some compounds may be illegal 
                in certain jurisdictions. Information about regulatory status is provided for educational 
                purposes only and does not constitute legal advice.
              </p>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">Self-Treatment Risks</h3>
              <p className="text-gray-700 mb-4">
                Self-treatment of any medical condition is dangerous and strongly discouraged. 
                The substances described may have serious side effects, contraindications, and interactions 
                with other medications. Never attempt to self-medicate based on information found on this site.
              </p>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">Research Focus</h3>
              <p className="text-gray-700 mb-4">
                This website focuses on preclinical and clinical research data. Research chemicals and 
                investigational compounds are inherently risky and should only be handled by qualified 
                researchers in appropriate laboratory settings.
              </p>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">Limitation of Liability</h3>
              <p className="text-gray-700">
                The operators of this website disclaim any liability for damages resulting from the use 
                or misuse of information contained herein. Use this information at your own risk.
              </p>
            </div>
          </div>
        </div>
      </main>
      
      <footer className="bg-white mt-8 py-6 border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            Information provided for educational purposes only. Not medical advice.
          </p>
        </div>
      </footer>
    </div>
  );
}