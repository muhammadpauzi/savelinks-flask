import { deleteLinkButtons, setStatusLinkButtons } from "./elements.js";

function getSpinner() {
    return `<div class="spinner-border spinner-border-sm spinner-grow-sm" role="status">
    <span class="visually-hidden">Loading...</span>
  </div>`
}

async function fetchLinks(url_suffix = '', options = {}) {
    const res = await fetch(`/links${url_suffix}`, options);
    const data = await res.json();
    return { res, data };
}

async function handleDeleteLink() {
    try {
        const id = this.dataset.id;
        this.innerHTML = getSpinner();
        const { res, data } = await fetchLinks(`/${id}/delete`, {
            method: "DELETE"
        });
        this.innerHTML = 'Delete'

        if (res.status == 200) {
            // hide the card
            this.parentElement.parentElement.parentElement.parentElement.remove();
        } else {
            alert('Cannot delete the link, please try again later!')
            console.log(data.message)
        }

    } catch (error) {
        alert("Something went wrong!");
        console.log(error.message)
    }
}

async function handleSetStatusLink() {
    try {
        const id = this.dataset.id;
        this.innerHTML = getSpinner();
        const { res, data } = await fetchLinks(`/${id}/status`, {
            method: "PUT"
        });
        if (res.status == 200) {
            const linkStatus = this.parentElement.parentElement.previousElementSibling.querySelector('.link-status');
            linkStatus.textContent = data.current_status;
            this.textContent = `Set to ${data.current_status == 'public' ? 'Private' : 'Public'}`;
        } else {
            alert('Cannot update the link, please try again later!')
            this.textContent = 'Error...';
            console.log(data.message)
        }

    } catch (error) {
        alert("Something went wrong!");
        console.log(error.message)
    }
}

deleteLinkButtons.forEach(button => {
    button.addEventListener('click', handleDeleteLink);
});

setStatusLinkButtons.forEach(button => {
    button.addEventListener('click', handleSetStatusLink);
});