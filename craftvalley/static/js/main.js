document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create-product-form');

    form.addEventListener('submit', function(event) {
        let valid = true;
        const fields = ['title', 'recipient', 'materials', 'category', 'description', 'price', 'amount', 'image'];
        const messages = [];

        fields.forEach(function(field) {
            const input = document.getElementById(field);
            if (!input.value) {
                valid = false;
                messages.push(`${field.charAt(0).toUpperCase() + field.slice(1)} is required.`);
            }
        });

        if (!valid) {
            event.preventDefault();
            alert(messages.join('\n'));
        }
    });
});
