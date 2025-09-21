import { useEffect, useRef } from 'react';

export const useAutoScroll = (dependencies: any[]) => {
  const isFirstRender = useRef(true);

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }

    const scrollAnchor = document.getElementById('scroll-anchor');
    if (scrollAnchor) {
      scrollAnchor.scrollIntoView({ behavior: 'smooth' });
    }
  }, dependencies);
};