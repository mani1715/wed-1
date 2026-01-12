import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import OpeningScreen from '@/components/invitation/OpeningScreen';
import InvitationContent from '@/components/invitation/InvitationContent';
import ParticleEffects from '@/components/invitation/ParticleEffects';

export const InvitationViewer = () => {
  const { design } = useParams();
  const navigate = useNavigate();
  const [showOpening, setShowOpening] = useState(true);
  const [deity, setDeity] = useState('ganesha'); // ganesha, venkateswara, shiva, none

  useEffect(() => {
    // Opening screen shows for 3 seconds
    const timer = setTimeout(() => {
      setShowOpening(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative min-h-screen overflow-x-hidden">
      {/* Opening Screen */}
      {showOpening && <OpeningScreen design={design} deity={deity} />}

      {/* Main Invitation Content */}
      {!showOpening && (
        <>
          <ParticleEffects design={design} />
          <InvitationContent design={design} deity={deity} />
          
          {/* Back Button */}
          <div className="fixed top-4 left-4 z-50">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/')}
              className="bg-white/80 backdrop-blur-sm hover:bg-white"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
          </div>
        </>
      )}
    </div>
  );
};

export default InvitationViewer;
