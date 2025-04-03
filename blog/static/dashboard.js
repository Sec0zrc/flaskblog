async function get_data(baseUrl, ...args) {
    if (args.length > 0) {
        // get the pagination data
        let page = args[0];
        let per_page = args[1];
        let result = undefined;
        let url = `${baseUrl}/api/v1/posts?page=${page}&per_page=${per_page}`
        const response = await fetch(url);
        if (response.ok) {
            console.log('response ok');
            result = await response.json();
            return result;
        } else {
            console.log('error');
            return false;
        }

    } else {
        // barely get the data
        let promise = await fetch(baseUrl, {
            method: 'GET', headers: {
                'Content-Type': 'application/json'
            }
        });
        if (promise.ok) {
            let data = await promise.json();
            return data;
        } else {
            console.log('error');
        }
    }


}

async function load_category() {
    let baseUrl = window.location.origin;
    let target = `${baseUrl}/api/v1/categories`
    let result = get_data(target);

    result.then(data => {
        let category_data = data.data;
        const category_container = document.querySelector('.list-group.list-group-flush.overflow-auto');
        category_container.innerHTML = '';
        for (let i = 0; i < category_data.length; i++) {
            let category_id = category_data[i].category_id;
            let category_name = category_data[i].category_name;
            const span = document.createElement('span');
            span.className = 'list-group-item d-flex align-items-center m-0';
            span.innerHTML = `<p class="m-0" >${category_name}</p>
                      <button class="btn btn-danger btn-sm ms-auto m-0" id=${category_id} onclick=delete_category(this)>删除</button>`;
            category_container.appendChild(span);
        }
    });
}

async function load_tag() {
    let baseUrl = window.location.origin;
    let target = `${baseUrl}/api/v1/tags`
    let result = get_data(target);
    // show tag_list in the website
    result.then(data => {
        let tag_data = data.data;
        const tag_container = document.querySelector('.tag-list.m-3');
        tag_container.innerHTML = '';
        for (let i = 0; i < tag_data.length; i++) {
            let tag_id = tag_data[i].tag_id;
            let tag_name = tag_data[i].tag_name;
            console.log(tag_name);
            const span = document.createElement('span');
            span.className = 'tag badge';
            span.innerHTML = `${tag_name}`;
            span.innerHTML += `<a href="#" class="btn-close" id='${tag_id}' onclick=delete_tag(this)></a>`;
            tag_container.appendChild(span);
        }
    });
}

async function add_category(category_name) {
    let baseUrl = window.location.origin;
    let target = `${baseUrl}/api/v1/categories`
    if (category_name === '') {
        alert('请输入分类名称');
        return;
    }
    let promise = await fetch(target, {
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({
            "category_name": category_name
        })
    });
    if (promise.ok) {
        let result = await promise.json();
        console.log(result);
        if (result.code === 201) {
            console.log('add category success');
            load_category();
            category_input.value = '';
        } else {
            console.log(`add category error ${result.error}`);
        }
    }
}

async function add_tag(tag_name) {
    if (tag_name === '') {
        alert('请输入标签名称');
        return;
    }
    let baseUrl = window.location.origin;
    let target = `${baseUrl}/api/v1/tags`
    let promise = await fetch(target, {
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({
            "tag_name": tag_name
        })
    });

    if (promise.ok) {
        let result = await promise.json();
        console.log(result)
        if (result.code === 201) {
            console.log('add tag success');
            load_tag();
            tag_input.value = '';
        } else {
            console.log(`add tag error ${result.error}`);
        }
    }
}

async function dashboard_load() {
    let baseUrl = window.location.origin;
    // get the count of posts
    let target1 = `${baseUrl}/api/v1/posts/count`
    let promise1 = get_data(target1);
    promise1.then(data => {
        let post_count = data.data['count'];
        const count_container = document.querySelector('#post_count');
        count_container.innerHTML = post_count;
    });


    // get the sketch count
    let target2 = `${baseUrl}/api/v1/posts/sketches/count`
    let promise2 = get_data(target2)
    promise2.then(data => {
        let skecth_count = data.data['count'];
        const count_container = document.querySelector('#sketch_count');
        count_container.innerHTML = skecth_count;
    });

    // get category list
    load_category();

    // get tag list
    load_tag();

    // add listener to add category button
    const category_input = document.querySelector('#category_input');
    const add_category_btn = category_input.nextElementSibling;
    add_category_btn.addEventListener('click', async () => {
        add_category(category_input.value)
    });

    // add listener to add tag button
    const tag_input = document.querySelector('#tag_input');
    const add_tag_btn = tag_input.nextElementSibling;
    add_tag_btn.addEventListener('click', async () => {
        add_tag(tag_input.value);
    });
}


async function delete_category(element) {
    let url = window.location.origin;
    let category_id = element.id;
    console.log(element);
    let tartget = `${url}/api/v1/categories/${category_id}`;
    let promise = await fetch(tartget, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json'
        }
    });
    let result = await promise.json();
    console.log(result);
    if (result.code === 200) {
        element.parentNode.remove();
        console.log('delete success');
    } else {
        console.log(`delete error ${result.error}`);
    }
}

async function delete_tag(element) {
    let url = window.location.origin;
    let tag_id = element.id;
    let tartget = `${url}/api/v1/tags/${tag_id}`;
    let promise = await fetch(tartget, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json'
        }
    });
    let result = await promise.json();
    if (result.code === 200) {
        element.parentNode.remove();
        console.log('delete success');
    } else {
        console.log(`delete error ${result.error}`);
    }
}

function logout() {
    fetch('/api/v1/logout', {
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.code === 200) {
                window.location.href = '/';
            }
        });
}

// pagination function 
function updatePagination(data) {
    const pagination_container = document.querySelector('.pagination.m-0.ms-auto');
    pagination_container.innerHTML = '';
    let current_page = data.data['page']
    let total_page = data.data['pages']

    // add prev button
    if (current_page > 1) {
        const prevButton = document.createElement('li');
        prevButton.className = 'page-item';
        prevButton.innerHTML = `            <a class="page-link" href="#" onclick="post_load(${current_page - 1})">
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
    // add page index
    for (let i = 1; i <= total_page; i++) {
        const pageButton = document.createElement('li');
        pageButton.className = 'page-item';
        pageButton.innerHTML = `<a class="page-link" href="#" onclick="post_load(${i})">${i}</a>`;
        pagination_container.appendChild(pageButton);
    }
    // add next button 
    if (current_page < total_page) {
        const nextButton = document.createElement('li');
        nextButton.className = 'page-item';
        nextButton.innerHTML = `<a class="page-link" href="#" onclick="post_load(${current_page + 1})">
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
async function post_load(page) {
    let baseUrl = window.location.origin;
    let per_page = 10;
    let result = get_data(baseUrl, page, per_page);
    result.then(data => {
        let post_list = data.data['posts'];
        const container = document.querySelector('#post_list');
        container.innerHTML = '';
        for (let i = 0; i < post_list.length; i++) {
            let post = post_list[i];
            const post_url = `target/${post.post_id}`
            const tr = document.createElement('tr');
            tr.innerHTML = `<td><span class="text-secondary">${post.post_id}</span></td>
                            <td><a href="invoice.html" class="text-reset" tabindex="-1">${post.title}</a></td>
                            <td>${post.category_id}</td>
                            <td>${post.tag_id}</td>`

            if(post.status === 0){
                // post is draft
                tr.innerHTML += `<td><span class="badge bg-yellow me-1"></span>草稿</td>`
            } else {
                tr.innerHTML += `<td><span class="badge bg-green me-1"></span>已发布</td>`
            }

            tr.innerHTML += `<td> ${post.create_at}</td>
                            <td class="text-end">
                            <a href="./dashboard-edit.html?edit=${post.post_id}" class="btn" role="button">编辑</a>
                            <a href="#" class="btn" role="button" onclick="delete_posts(${post.post_id})">删除</a>
                            </td>`

            container.appendChild(tr);
        }
        updatePagination(data);
    });

}