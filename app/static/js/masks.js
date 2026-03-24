// Máscara para CPF: XXX.XXX.XXX-XX
function maskCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length > 11) cpf = cpf.slice(0, 11);
    
    if (cpf.length <= 3) {
        return cpf;
    } else if (cpf.length <= 6) {
        return cpf.slice(0, 3) + '.' + cpf.slice(3);
    } else if (cpf.length <= 9) {
        return cpf.slice(0, 3) + '.' + cpf.slice(3, 6) + '.' + cpf.slice(6);
    } else {
        return cpf.slice(0, 3) + '.' + cpf.slice(3, 6) + '.' + cpf.slice(6, 9) + '-' + cpf.slice(9);
    }
}

// Máscara para Telefone: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
function maskPhone(phone) {
    phone = phone.replace(/\D/g, '');
    if (phone.length > 11) phone = phone.slice(0, 11);
    
    if (phone.length <= 2) {
        return phone;
    } else if (phone.length <= 7) {
        return '(' + phone.slice(0, 2) + ') ' + phone.slice(2);
    } else {
        return '(' + phone.slice(0, 2) + ') ' + phone.slice(2, 7) + '-' + phone.slice(7);
    }
}

// Aplicar máscaras aos campos
document.addEventListener('DOMContentLoaded', function() {
    // Máscara para CPF
    const cpfInputs = document.querySelectorAll('input[name="cpf"], input[id*="cpf"]');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = maskCPF(this.value);
        });
    });

    // Máscara para Telefone
    const phoneInputs = document.querySelectorAll('input[name="telefone"], input[id*="telefone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = maskPhone(this.value);
        });
    });
});
