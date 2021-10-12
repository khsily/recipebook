import { useCallback, useEffect, useState } from 'react';
import * as SplashScreen from 'expo-splash-screen';

export function useSplash(beforeReady) {
    const [appIsReady, setAppIsReady] = useState(false);

    useEffect(() => {
        async function prepare() {
            try {
                await SplashScreen.preventAutoHideAsync();
                await beforeReady();
            } catch (e) {
                console.warn(e);
            } finally {
                setAppIsReady(true);
                await SplashScreen.hideAsync();
            }
        }

        prepare();
    }, []);

    return appIsReady;
}