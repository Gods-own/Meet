document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.sideform').addEventListener('submit', function(e) {
        e.preventDefault()
        document.querySelector('.search-append').innerHTML = ""
        sidebar_search()
        document.querySelector('.side-search').value = "";
    })

    
})

function sidebar_search() {
    let searchvalue = document.querySelector('.side-search').value
    if (searchvalue.trim()) {
        fetch(`/sidesearch?q=${searchvalue}`)
        .then(response => response.json())
        .then(data => {
            let names = data
            // console.log(names)
            if(names.person) {
                console.log(names, "j")
                let element = document.createElement('div')
                element.innerHTML = `
                    <p class="notfound">No names found</p>
                `
                document.querySelector('.search-append').append(element)
                element.className = "search-results"
            }
            else if(Array.isArray(names)) {
                names.forEach(function(name) {
                    let element = document.createElement('div')
                    console.log(name)
                element.innerHTML = `
                    <div>
                        <img src="${name.userImage}">
                    </div>
                    <div>
                        <h3><a style="color: black;" href="/profile/${name.id}">${name.username}</a></h3>
                    </div>
                `
                element.className = "search-results"
                document.querySelector('.search-append').append(element)
                })
            }
            else {
                console.log(names, "h")
                let element = document.createElement('div')
                element.innerHTML = `
                    <div>
                        <img src=${names.userImage}>
                    </div>
                    <div>
                        <h3><a style="color: black;" href="/profile/${names.id}">${names.username}</a></h3>
                    </div>
                `
                element.className = "search-results"
                document.querySelector('.search-append').append(element)
            }
        })
    }
    else {
        let element = document.createElement('div')
                element.innerHTML = `
                    <p class="notfound">No names found</p>
                `
                document.querySelector('.search-append').append(element)
                element.className = "search-results"
    }
}