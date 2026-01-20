import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Heart, Calendar, Users, Share2, Globe, Clock } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-purple-50">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <Heart className="w-16 h-16 mx-auto text-rose-500 mb-6" />
          <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-6">
            Beautiful Wedding Invitations
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Create stunning, personalized digital invitations for weddings, engagements, and special celebrations.
            Share with your loved ones instantly.
          </p>
          <Button
            size="lg"
            onClick={() => navigate('/admin/login')}
            className="bg-rose-500 hover:bg-rose-600 text-white px-8 py-6 text-lg"
          >
            Admin Login
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto mt-20">
          <FeatureCard
            icon={<Calendar className="w-12 h-12 text-rose-500" />}
            title="Multiple Event Types"
            description="Create invitations for marriages, engagements, and birthday celebrations with ease."
          />
          <FeatureCard
            icon={<Globe className="w-12 h-12 text-purple-500" />}
            title="Multi-Language Support"
            description="Choose from Telugu, Hindi, Tamil, or English to match your cultural preferences."
          />
          <FeatureCard
            icon={<Share2 className="w-12 h-12 text-pink-500" />}
            title="Easy Sharing"
            description="Generate unique links that can be shared instantly with family and friends."
          />
          <FeatureCard
            icon={<Users className="w-12 h-12 text-rose-500" />}
            title="Guest Greetings"
            description="Collect heartfelt wishes and messages from your guests in one beautiful place."
          />
          <FeatureCard
            icon={<Clock className="w-12 h-12 text-purple-500" />}
            title="Link Expiry Control"
            description="Set custom expiry dates for your invitation links or make them permanent."
          />
          <FeatureCard
            icon={<Heart className="w-12 h-12 text-pink-500" />}
            title="Beautiful Designs"
            description="Gorgeous, mobile-responsive designs that look stunning on any device."
          />
        </div>

        {/* CTA Section */}
        <div className="text-center mt-20">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            Ready to create your perfect invitation?
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Contact us to get started with your personalized wedding invitation platform.
          </p>
          <div className="flex justify-center gap-4">
            <Button
              variant="outline"
              size="lg"
              className="border-rose-500 text-rose-500 hover:bg-rose-50"
            >
              Contact Us
            </Button>
            <Button
              size="lg"
              onClick={() => navigate('/admin/login')}
              className="bg-rose-500 hover:bg-rose-600 text-white"
            >
              Admin Access
            </Button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20 py-8">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© 2025 Wedding Invitations Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }) => {
  return (
    <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-xl transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default LandingPage;
