import Link from 'next/link';

export default function CatalogPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Substance Catalog</h1>
          <nav>
            <Link href="/" className="text-blue-600 hover:text-blue-800 mr-6">Home</Link>
            <Link href="/blog" className="text-blue-600 hover:text-blue-800 mr-6">Blog</Link>
            <Link href="/about" className="text-blue-600 hover:text-blue-800">About</Link>
          </nav>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Filter Substances</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <select className="border border-gray-300 rounded-md p-2">
                  <option>All Classes</option>
                  <option>Actoprotectors</option>
                  <option>Dopamine Agonists</option>
                  <option>Vitamin Derivatives</option>
                  <option>ISR Modulators</option>
                </select>
                
                <select className="border border-gray-300 rounded-md p-2">
                  <option>All Targets</option>
                  <option>TH (Tyrosine Hydroxylase)</option>
                  <option>eIF2B</option>
                  <option>D2/D3 Receptors</option>
                  <option>AhR (Aryl Hydrocarbon Receptor)</option>
                  <option>Telomerase</option>
                </select>
                
                <select className="border border-gray-300 rounded-md p-2">
                  <option>All Phases</option>
                  <option>Preclinical</option>
                  <option>Phase I</option>
                  <option>Phase II</option>
                  <option>Phase III</option>
                  <option>FDA Approved</option>
                </select>
              </div>
            </div>
            
            <div className="mt-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Available Substances</h2>
              <div className="space-y-4">
                <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <h3 className="text-lg font-medium text-gray-900">Bromantane</h3>
                  <p className="text-gray-600">Actoprotector with dopaminergic properties</p>
                  <div className="mt-2 flex space-x-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Actoprotector
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      D2/D3 Partial Agonist
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      Preclinical
                    </span>
                  </div>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <h3 className="text-lg font-medium text-gray-900">Pramipexole</h3>
                  <p className="text-gray-600">Dopamine D2/D3 receptor agonist</p>
                  <div className="mt-2 flex space-x-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Dopamine Agonist
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      D2/D3 Full Agonist
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                      FDA Approved
                    </span>
                  </div>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <h3 className="text-lg font-medium text-gray-900">ISRIB</h3>
                  <p className="text-gray-600">Integrated Stress Response Inhibitor</p>
                  <div className="mt-2 flex space-x-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      ISR Modulator
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      eIF2B Activator
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      Preclinical
                    </span>
                  </div>
                </div>
              </div>
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