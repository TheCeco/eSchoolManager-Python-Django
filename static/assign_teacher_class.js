let teacher = document.getElementById('id_teacher');
let subject = document.getElementById('id_subject');


subject.addEventListener('click', function () {
        let teacher_pk = Number(document.getElementById('id_teacher').value);
        let needed_subjects = []

        for (let i = 0; i < teachersSubject.length; i++) {
            if (teachersSubject[i][teacher_pk] !== undefined) {
                needed_subjects.push(teachersSubject[i][teacher_pk])
            }
        }

        for (let i = 0; i < subject.options.length; i++) {
            if (!needed_subjects.includes(subject.options[i].text)) {
                subject.options[i].style.display = 'none'
            }
        }

        console.log(subject.options);
    }
)

teacher.addEventListener('click', function () {
    for (let i = 0; i < subject.options.length; i++) {
        subject.options[i].style.display = ''
    }
})

window.addEventListener('load', function () {
    let error_div = document.getElementsByClassName('form-group')[3]
    let error_message = document.getElementsByClassName('errorlist')[1]

    error_div.removeChild(document.getElementsByClassName('errorlist')[0])
    error_div.appendChild(error_message)
})