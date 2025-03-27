async function getData(baseUrl, page, per_page) {
    console.log('getData');
    console.log(baseUrl);
    let result = undefined;
    let url = `${baseUrl}/api/v1/posts?page=${page}&per_page=${per_page}`
    const response = await fetch(url);
    if (response.ok) {
        console.log('response ok');
        result = await response.json();
    } else {
        console.log('error');
    }
    return result;
}

function updatePagination(data) {
    const pagination_container = document.querySelector('.pagination.m-0.ms-auto');
    pagination_container.innerHTML = '';
    let current_page = data.data['page']
    let total_page = data.data['pages']
    console.log(pagination_container);
    console.log(current_page);
    console.log(total_page);
    if (current_page > 1) {
        const prevButton = document.createElement('li');
        prevButton.className = 'page-item';
        prevButton.innerHTML = `            <a class="page-link" href="#" onclick="load_page(${current_page - 1})">
                <!-- Download SVG icon from http://tabler.io/icons/icon/chevron-left -->
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" class="icon icon-1">
                    <path d="M15 6l-6 6l6 6"></path>
                </svg>
                prev
            </a>`;
        pagination_container.appendChild(prevButton);
    }
    for (let i = 1; i <= total_page; i++) {
        const pageButton = document.createElement('li');
        pageButton.className = 'page-item';
        pageButton.innerHTML = `<a class="page-link" href="#" onclick="load_page(${i})">${i}</a>`;
        pagination_container.appendChild(pageButton);
    }
    if (current_page < total_page) {
        const nextButton = document.createElement('li');
        nextButton.className = 'page-item';
        nextButton.innerHTML = `<a class="page-link" href="#" onclick="load_page(${current_page + 1})">
                                    next
                                    <!-- Download SVG icon from http://tabler.io/icons/icon/chevron-right -->
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                        stroke-linejoin="round" class="icon icon-1">
                                        <path d="M9 6l6 6l-6 6"></path>
                                    </svg>
                                </a>`;
        pagination_container.appendChild(nextButton);
    }
}

function load_page(page) {
    const baseUrl = 'http://127.0.0.1:5000';
    const per_page = 10;
    let promise = getData(baseUrl, page, per_page);
    promise.then(data => {
        const container = document.querySelector('.row.row-cards.mb-3');
        container.innerHTML = '<h3 class="mb-0">最新文章 <span class="badge">new</span></h3>';
        let posts_list = data.data['posts'];
        console.log(data)
        for (let i = 0; i < posts_list.length; i++) {
            let post = posts_list[i];
            const current_url = window.location.path;
            console.log(current_url);
            const card = document.createElement('div');
            card.className = 'card card-sm ms-auto';
            card.innerHTML += `<div class="card-body">
                                <a href="/posts.html?post_id=${post.post_id}" class="link">
                                    <span class="title">${post.title}</span>
                                </a>
                                <spane class="float-end">${post.create_at}</span>
                            </div>
                        </div>`
            container.appendChild(card);
        }
        console.log(container);
        updatePagination(data);
    });
}

document.addEventListener('DOMContentLoaded',
    function () {
        load_page(1)
    });
