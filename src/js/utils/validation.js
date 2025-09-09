export const validators = {
    required: (value) => {
        return value !== undefined && value !== null && value !== '';
    },
    
    email: (value) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(value);
    },
    
    minLength: (value, min) => {
        return value.length >= min;
    },
    
    maxLength: (value, max) => {
        return value.length <= max;
    },
    
    numeric: (value) => {
        return !isNaN(value);
    },
    
    date: (value) => {
        const date = new Date(value);
        return date instanceof Date && !isNaN(date);
    }
};

export const validateForm = (data, rules) => {
    const errors = {};
    
    for (const field in rules) {
        const fieldRules = rules[field];
        const value = data[field];
        
        for (const rule of fieldRules) {
            const [validatorName, ...params] = rule.split(':');
            const validator = validators[validatorName];
            
            if (validator && !validator(value, ...params)) {
                errors[field] = rule.message || `Campo inválido`;
                break;
            }
        }
    }
    
    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
};