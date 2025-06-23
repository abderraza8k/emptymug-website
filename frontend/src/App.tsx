import React from 'react';
import Hero from './components/Hero';
import ContactForm from './components/ContactForm';
import './index.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <Hero />
      <ContactForm />
      
      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-6 text-center">
          <div className="flex items-center justify-center mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white text-xl font-bold">EM</span>
            </div>
            <span className="text-2xl font-bold">EmptyMug</span>
          </div>
          <p className="text-gray-400 mb-6">Creating digital experiences that matter</p>
          <div className="border-t border-gray-800 pt-6">
            <p className="text-gray-500">
              © 2025 EmptyMug. Built with ❤️ using React & Python.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
