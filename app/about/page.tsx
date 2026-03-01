export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">About NeuroPharma Catalog</h1>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="prose max-w-none">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Scientific-Analytical Approach</h2>
              
              <p className="text-gray-700 mb-4">
                The NeuroPharma Catalog is a scientific-analytical resource focused on neuropharmacological substances, 
                their mechanisms of action, and evidence-based research. Our approach emphasizes critical analysis over marketing rhetoric.
              </p>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">Target Audience</h3>
              <ul className="list-disc pl-6 text-gray-700 mb-4">
                <li>Medical professionals</li>
                <li>Pharmacologists and researchers</li>
                <li>Neurobiologists</li>
                <li>Advanced biohacking specialists</li>
                <li>Senior medical/biology students</li>
              </ul>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">Content Philosophy</h3>
              <ul className="list-disc pl-6 text-gray-700 mb-4">
                <li>Strict analytical approach without promotional tone</li>
                <li>Focus on mechanisms of action and signal cascades</li>
                <li>Critical review of contradictions and limitations</li>
                <li>Evidence level indication for all claims</li>
                <li>Emphasis on risks and side effects</li>
              </ul>
              
              <h3 className="text-xl font-medium text-gray-800 mt-6 mb-3">Scientific Rigor</h3>
              <p className="text-gray-700 mb-4">
                All information is based on peer-reviewed research, clinical trials, and preclinical studies. 
                We clearly distinguish between different phases of development and regulatory status.
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