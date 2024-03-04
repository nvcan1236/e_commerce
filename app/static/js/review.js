const closeBtn = document.querySelector('.close-modal')
const modal = document.getElementById('review-modal')

function closeModal() {
    modal.classList.add('hide')
}

function openModal() {
    modal.classList.remove('hide')
    if (modal.classList.contains('hide')) {
    }
}

function showFormReply(formId) {
    const formReply = document.getElementById(formId)
    formReply.classList.remove('hide')
}

function sendReview(productId, customerId, detailId) {
    content = document.getElementById(`review-for-${productId}`).value
    fetch('/api/review', {
        headers: {
            'Content-Type': "application/json"
        },
        method: 'POST',
        body: JSON.stringify({
            productId,
            content,
            customerId,
            detailId
        })

    }).then(res => res.json())
        .then(data => alert(data.message))
        .catch(err => alert(err))
        .finally(()=> closeModal())
}