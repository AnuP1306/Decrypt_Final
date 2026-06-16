import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Get these values from:
// Firebase Console -> Project Settings -> General -> Your apps -> Web app (</> icon)
const firebaseConfig = {
    apiKey: "AIzaSyDfVRHh1CyuAaflxyiN4tBhb3K0LbzoWHg",
    authDomain: "decrypt-auth-b999d.firebaseapp.com",
    projectId: "decrypt-auth-b999d",
    storageBucket: "decrypt-auth-b999d.firebasestorage.app",
    messagingSenderId: "1073105747493",
    appId: "1:1073105747493:web:1ec52e11227f72e8d209cc",
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
export default app;