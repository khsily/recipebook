import { useRef } from 'react';

export function useScrollTop() {
    const scrollRef = useRef();

    const scrollToTop = (animated = true) => {
        scrollRef.current.scrollToOffset({ animated, offset: 0 });
    }

    return [scrollRef, scrollToTop];
}