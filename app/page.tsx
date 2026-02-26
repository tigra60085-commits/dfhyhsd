import Link from 'next/link';
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'NeuroPharma Catalog',
  description: 'Scientific-analytical catalog of neuropharmacological substances',
}

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">NeuroPharma Catalog</h1>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="text-center mb-10">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Scientific-Analytical Catalog of Neuropharmacological Substances</h2>
              <p className="text-gray-600 max-w-3xl mx-auto">
                Evidence-based analysis of neuroactive compounds, their mechanisms of action, and research findings. 
                Focused on scientific rigor rather than marketing claims.
              </p>
            </div>
            
            <div className="mt-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Substance Catalog</h3>
                  <p className="text-gray-600 mb-4">
                    Comprehensive database of neuroactive compounds with detailed mechanism analysis, 
                    pharmacokinetics, and clinical data.
                  </p>
                  <Link href="/catalog" className="text-blue-600 hover:text-blue-800 font-medium">
                    Browse Catalog →
                  </Link>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Analytical Blog</h3>
                  <p className="text-gray-600 mb-4">
                    Critical reviews of research, analysis of mechanisms, and examination of contradictions 
                    in neuropharmacological studies.
                  </p>
                  <Link href="/blog" className="text-blue-600 hover:text-blue-800 font-medium">
                    Read Articles →
                  </Link>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Research Focus</h3>
                  <p className="text-gray-600 mb-4">
                    Deep dives into specific areas including neuroplasticity, stress response, 
                    dopaminergic systems, and novel therapeutic approaches.
                  </p>
                  <Link href="/blog" className="text-blue-600 hover:text-blue-800 font-medium">
                    Explore Topics →
                  </Link>
                </div>
              </div>
            </div>
            
            <div className="mt-12">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Additions to Catalog</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Substance</th>
                      <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class</th>
                      <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Primary Target</th>
                      <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Evidence Level</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">Bromantane</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                          Actoprotector
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">D2/D3 Dopamine Receptors</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Preclinical</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">Pramipexole</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          Dopamine Agonist
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">D2/D3 Dopamine Receptors</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">FDA Approved</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">ISRIB</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                          ISR Modulator
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">eIF2B</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Preclinical</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div className="mt-12">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Featured Analytical Articles</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <h3 className="font-medium text-gray-900">Why Genomic Induction of Dopamine Is Not the Same as Stimulation</h3>
                  <p className="text-sm text-gray-600 mt-1">Critical analysis of molecular mechanisms and therapeutic implications</p>
                </div>
                <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <h3 className="font-medium text-gray-900">ISR: Protective Mechanism or Pathology?</h3>
                  <p className="text-sm text-gray-600 mt-1">Examining the dual nature of the Integrated Stress Response</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      <footer className="bg-white mt-8 py-6 border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-600 text-sm mb-2">
              Information provided for educational purposes only. Not medical advice.
            </p>
            <div className="flex justify-center space-x-6">
              <Link href="/legal" className="text-sm text-gray-500 hover:text-gray-700">
                Legal Disclaimer
              </Link>
              <Link href="/about" className="text-sm text-gray-500 hover:text-gray-700">
                About Project
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
