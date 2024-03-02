const closeBtn = document.querySelector('.close-modal')
const modal = document.getElementById('review-modal')

function closeModal() {
    modal.classList.add('hide')
}

function openModal() {
    modal.classList.remove('hide')
    if(modal.classList.contains('hide')) {
    }
}

function showFormReply(formId) {
    const formReply = document.getElementById(formId)
    formReply.classList.remove('hide')
}