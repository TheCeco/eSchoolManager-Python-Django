document.getElementsByTagName('select')[0].addEventListener('change', function () {

    let selectedSubject = this.value
    let tables = document.getElementsByClassName('grades')

    for (let i = 0; i < tables.length; i++) {
        tables[i].style.display = 'none'
    }

    if (selectedSubject) {
        let selectedTable = document.getElementById(selectedSubject + '-table')
        if (selectedTable){
            selectedTable.style.display = 'table'
        }
    }
})
