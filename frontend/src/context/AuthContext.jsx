// src/context/AuthContext.jsx
import { createContext, useContext, useEffect, useState } from "react";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signInWithPopup,
    GoogleAuthProvider,
    GithubAuthProvider,
    onAuthStateChanged,
    signOut,
    updateProfile,
} from "firebase/auth";
import { doc, setDoc, getDoc, serverTimestamp } from "firebase/firestore";
import { auth, db } from "../firebase";

const AuthContext = createContext();

// Custom hook so any component can do: const { currentUser, login } = useAuth();
export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }) {
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Creates the Firestore user doc the first time someone signs up
    // (works for email/password AND Google/GitHub, since social logins
    // don't go through our handleSignup form)
    const createUserDocIfNeeded = async (user, extraData = {}) => {
        const userRef = doc(db, "users", user.uid);
        const snapshot = await getDoc(userRef);

        if (!snapshot.exists()) {
            await setDoc(userRef, {
                name: user.displayName || extraData.name || "",
                email: user.email,
                createdAt: serverTimestamp(),
                onboardingCompleted: false,
                personalization: {
                    vibe: "", // Step 1: "What's your vibe?" -> e.g. "AI"
                    knowledgeLevel: "", // Step 2: beginner / intermediate / advanced
                    interests: [], // Step 3: multi-select topics
                },
                ...extraData,
            });
            return true; // isNewUser
        }
        return false;
    };

    // ---- Email/Password Signup ----
    const signup = async (name, email, password) => {
        const result = await createUserWithEmailAndPassword(auth, email, password);
        await updateProfile(result.user, { displayName: name });

        // Manually create the doc with name directly — don't rely on displayName
        const userRef = doc(db, "users", result.user.uid);
        try {
            await setDoc(userRef, {
                name: name,  // ← use name directly from form, not result.user.displayName
                email: email,
                createdAt: serverTimestamp(),
                onboardingCompleted: false,
                personalization: {
                    vibe: "",
                    knowledgeLevel: "",
                    interests: [],
                },
            });
            console.log("✅ Firestore doc created successfully");
        } catch (err) {
            console.error("❌ Firestore doc creation failed:", err.message);
        }

        return result.user;
    };
    // ---- Email/Password Login ----
    const login = (email, password) => {
        return signInWithEmailAndPassword(auth, email, password);
    };

    // ---- Google Login/Signup ----
    const googleLogin = async () => {
        const provider = new GoogleAuthProvider();
        const result = await signInWithPopup(auth, provider);
        const isNewUser = await createUserDocIfNeeded(result.user);
        return { user: result.user, isNewUser };
    };

    // ---- GitHub Login/Signup ----
    const githubLogin = async () => {
        const provider = new GithubAuthProvider();
        const result = await signInWithPopup(auth, provider);
        const isNewUser = await createUserDocIfNeeded(result.user);
        return { user: result.user, isNewUser };
    };

    const logout = () => signOut(auth);

    // Keeps currentUser in sync across the whole app (refresh, tab reopen, etc.)
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            setCurrentUser(user);
            setLoading(false);
        });
        return unsubscribe;
    }, []);

    const value = {
        currentUser,
        signup,
        login,
        googleLogin,
        githubLogin,
        logout,
    };

    // Don't render the app until we know whether someone is logged in,
    // otherwise protected routes will flash/redirect incorrectly
    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}
