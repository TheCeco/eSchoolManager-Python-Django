window.addEventListener('load', function () {
    let error_row = document.getElementsByClassName('row')[2]
    let error_message = document.getElementsByClassName('errorlist')[1]

    error_row.removeChild(document.getElementsByClassName('errorlist')[0])
    error_row.appendChild(error_message)
})