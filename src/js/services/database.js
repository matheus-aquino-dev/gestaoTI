import { getFirestore, collection, doc, addDoc, getDoc, getDocs, updateDoc, deleteDoc, query, where } from 'firebase/firestore';

const db = getFirestore();

// Funções genéricas CRUD
export const createDocument = async (collectionName, data) => {
    try {
        const docRef = await addDoc(collection(db, collectionName), {
            ...data,
            createdAt: new Date(),
            updatedAt: new Date()
        });
        return docRef.id;
    } catch (error) {
        throw new Error(`Erro ao criar documento: ${error.message}`);
    }
};

export const readDocument = async (collectionName, id) => {
    try {
        const docRef = doc(db, collectionName, id);
        const docSnap = await getDoc(docRef);
        
        if (docSnap.exists()) {
            return { id: docSnap.id, ...docSnap.data() };
        }
        return null;
    } catch (error) {
        throw new Error(`Erro ao ler documento: ${error.message}`);
    }
};

export const updateDocument = async (collectionName, id, data) => {
    try {
        const docRef = doc(db, collectionName, id);
        await updateDoc(docRef, {
            ...data,
            updatedAt: new Date()
        });
        return true;
    } catch (error) {
        throw new Error(`Erro ao atualizar documento: ${error.message}`);
    }
};

export const deleteDocument = async (collectionName, id) => {
    try {
        const docRef = doc(db, collectionName, id);
        await deleteDoc(docRef);
        return true;
    } catch (error) {
        throw new Error(`Erro ao deletar documento: ${error.message}`);
    }
};

export const listDocuments = async (collectionName, filters = []) => {
    try {
        let q = collection(db, collectionName);
        
        if (filters.length > 0) {
            q = query(q, ...filters.map(f => where(f.field, f.operator, f.value)));
        }
        
        const querySnapshot = await getDocs(q);
        return querySnapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }));
    } catch (error) {
        throw new Error(`Erro ao listar documentos: ${error.message}`);
    }
};