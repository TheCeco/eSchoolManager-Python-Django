window.addEventListener('load', function () {
    let phone = document.getElementById('id_phone')

    let today_year = new Date().getFullYear()
    let profile_date = document.getElementById('id_date_of_birth')
    let profile_year = Number(profile_date.value.slice(0, 4))

    let first_name = document.getElementById('id_first_name')
    let last_name = document.getElementById('id_last_name')

    let phone_ul = document.createElement('ul')
    phone_ul.classList.add('errorlist')

    let date_ul = document.createElement('ul')
    date_ul.classList.add('errorlist')

    let names_ul = document.createElement('ul')
    names_ul.classList.add('errorlist')


    if (phone.value !== '') {
        // Checking if phone number starts with "0" and is 10 chars long
        // Checking if phone number starts with "+" and is 13 chars long
        if ((phone.value.length !== 10 || !phone.value.startsWith('0'))
            && (phone.value.length !== 13 || !phone.value.startsWith('+'))) {

            let valid_phone_li = document.createElement('li')
            valid_phone_li.textContent = 'Phone number must starts with "0" and be 10 chars long or starts with "+" and be 13 chars long'
            phone_ul.appendChild(valid_phone_li)
            phone.parentElement.appendChild(phone_ul)
        }

        // Checking for letters in phone number
        if (/[a-zA-Z]+/.test(phone.value)) {

            let no_char_li = document.createElement('li')
            no_char_li.textContent += 'The phone number cannot contain letters'
            phone_ul.appendChild(no_char_li)
            phone.parentElement.appendChild(phone_ul)
        }
    }

    // Checking for numbers in first and last name
    if (/[0-9]+/.test(first_name.value) || /[0-9]+/.test(last_name.value)) {
        let valid_name_li = document.createElement('li')
        valid_name_li.textContent = 'Name fields cannot contain nums'
        names_ul.appendChild(valid_name_li)
        first_name.parentElement.appendChild(names_ul)
    }

    // Checking if the year is valid
    console.log(profile_date.value)
    if (profile_date.value !== '') {
        if ((today_year - profile_year) > 100 || (profile_year >= today_year)) {

            let valid_year_li = document.createElement('li')
            valid_year_li.textContent = `Please enter a valid year from ${today_year - 100} to ${today_year - 1}`
            date_ul.appendChild(valid_year_li)
            profile_date.parentElement.appendChild(date_ul)
        }
    }

})