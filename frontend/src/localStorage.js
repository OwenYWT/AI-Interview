export const setItem = (key, value) => {
    localStorage.setItem(key, JSON.stringify(value));
};

export const getItem = (key, defaultValue = null) => {
    const storedValue = localStorage.getItem(key);
    return storedValue ? JSON.parse(storedValue) : defaultValue;
};

export const removeItem = (key) => {
    localStorage.removeItem(key);
};
