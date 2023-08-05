let UserTypeField = document.getElementById('id_user_type')

let schoolClassLabel = document.getElementsByTagName('label')[4]
let schoolClassField = document.getElementById('id_school_class')

function toggleSubjectField() {
    if (UserTypeField.value === 'student') {
        schoolClassField.style.display = '';
        schoolClassField.required = true
        schoolClassLabel.style.display = '';
    } else {
        schoolClassField.style.display = 'none';
         schoolClassField.required = false
        schoolClassLabel.style.display = 'none';
    }
}

toggleSubjectField()

window.addEventListener('change', function () {
    toggleSubjectField();
})