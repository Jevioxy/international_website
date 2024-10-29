document.addEventListener('DOMContentLoaded', function () {
    const userSelect = document.querySelector('#id_user');
    const emailField = document.querySelector('#id_email');

    if (userSelect && emailField) {
        userSelect.addEventListener('change', function () {
            const userId = userSelect.value;
            if (userId) {
                fetch(`/admin/get_user_email/${userId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.email) {
                            emailField.value = data.email;
                        } else {
                            emailField.value = '';
                        }
                    });
            } else {
                emailField.value = '';
            }
        });
    }
});
