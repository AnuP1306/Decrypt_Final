import { doc, updateDoc } from "firebase/firestore";
import { db } from "../firebase";

export async function saveOnboarding(uid, { vibe, knowledgeLevel, interests }) {
    const userRef = doc(db, "users", uid);

    await updateDoc(userRef, {
        "personalization.vibe": vibe,
        "personalization.knowledgeLevel": knowledgeLevel,
        "personalization.interests": interests,
        onboardingCompleted: true,
    });
}