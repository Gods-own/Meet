document.addEventListener("DOMContentLoaded", function() { 

    document.querySelector('.close-btn').addEventListener('click', function() {
        document.querySelector('.modal').style.display = 'none';
    })

    // document.querySelector('.modal').addEventListener('click', function(e) {
    //     e.stopImmediatePropagation()
    //     e.stopPropagation()
    //     document.querySelector('.modal').style.display = 'none';
    // })

    console.log('article')
    document.querySelectorAll('.uncolored-heart').forEach(function(likeBtn) {
        likeBtn.addEventListener('click', function() {
                let activityid;
                let str = likeBtn.dataset.id 
                strlen = str.length - 9
                
                activityid = str.substring(0, strlen)
                // activityid = str.charAt(0)
                likepost(activityid)
                document.querySelector(`[data-id="${activityid}colored"]`).classList.toggle('show-inline')
                likeBtn.classList.toggle('hide')
        })
    })
    
    document.querySelectorAll('.colored-heart').forEach(function(likeBtn) {
        likeBtn.addEventListener('click', function() {
            let activityid;
            let str = likeBtn.dataset.id 
            strlen = str.length - 7
                
            activityid = str.substring(0, strlen)
            // activityid = str.charAt(0)
            console.log(activityid)
            likepost(activityid)
            document.querySelector(`[data-id="${activityid}uncolored"]`).classList.toggle('hide')
            likeBtn.classList.toggle('show-inline')
        })
    })

    document.querySelectorAll('.card').forEach(function(activitycard) {
        activitycard.addEventListener('click', function() {
                let activityid;
                let str = activitycard.dataset.id;
                
                activityid = str
                // activityid = str.charAt(0)
                document.querySelector('.modal-body').innerHTML = '';
                viewpost(activityid)
        })
    })
    
})

function viewpost(activityid) {
    fetch("/post/"+activityid)
    .then(response => response.json())
    .then(data => {
        document.querySelector(".modal").style.display = 'block';
        let element = document.createElement('article');
        console.log(data)
        element.className = "post-view-article";
        element.innerHTML = `
   		<header class="post-view-header">
   			<div>
                <img src="${data.posterImage}">
                <h3>${data.poster}</h3>
            </div>
            <a class="edit-btn">Edit</a>
   		</header>
   		<img class="post-view-img" src="${data.picture}">
   		<div class="post-view-body">
   			<p><strong>${data.hobby}</strong></p>
   			<p class="activity-caption">${data.activity}</p>  
   			<div class="post-view-btns">
   				<div>
   					<a class="like-buttons">
		            <button class="colored-heart btn-icon"><i class="las la-heart" data-id="${data.id}colored" aria-hidden="true"></i></button>
                    <button data-id="${data.id}uncolored" class="uncolored-heart btn-icon"><i class="lar la-heart"></i></button>
		            <small class="show-like">${data.likes}</small>
		        </a>
   				</div>
   				<div class="post-view-msg-btn">
   					<button><a>Message</a></button>
   				</div>
   			</div>
   		</div>
           <form class="editpost-form">
    <div class="form-group">
        <label for="caption">Caption</label>
        <textarea class="form-control" id="caption" name="caption">${data.activity}</textarea>
    </div>
    <div>
        <button class="btn btn-success" type="submit">Submit</button>
    </div>
</form>`
        document.querySelector('.modal-body').append(element)
        let color = element.closest('.colored-heart')
        let uncolor = element.closest('.uncolored-heart')
        let caption = document.querySelector('.activity-caption')
        let postid = data.id;
        checklike(postid, color, uncolor)
        element.addEventListener('click', function(e) {
            if (e.target.closest('.colored-heart')) {
                let nolikes = e.target.closest('.colored-heart').nextElementSibling.nextElementSibling;
                let activityid;
                // let str = e.target.closest('.colored-heart').dataset.id 
                // strlen = str.length - 7
                    
                // activityid = str.substring(0, strlen)
                activityid = data.id;
                console.log(activityid)
                likepost(activityid, nolikes)
                e.target.closest('.colored-heart').nextElementSibling.classList.toggle('hide')
                e.target.closest('.colored-heart').classList.toggle('show-inline')
            }
        })

        element.addEventListener('click', function(e) {
            if (e.target.closest('.uncolored-heart')) {
                let nolikes = e.target.closest('.uncolored-heart').nextElementSibling;
                let activityid;
                // let str = e.target.closest('.uncolored-heart').dataset.id 
                // strlen = str.length - 9
                
                // activityid = str.substring(0, strlen)
                activityid = data.id;
                likepost(activityid, nolikes)
                e.target.closest('.uncolored-heart').previousElementSibling.classList.toggle('show-inline')
                e.target.closest('.uncolored-heart').classList.toggle('hide')
            }
        })

        element.addEventListener('click', function(e) {
            if (e.target.closest('.edit-btn')) {
                document.querySelector(`.post-view-body`).classList.toggle('hide');
                document.querySelector(`.editpost-form`).classList.toggle('show');
            }
        })

        element.addEventListener('submit', function(e) {
            e.preventDefault()
            e.stopImmediatePropagation()
            if (e.target.closest('form')) {
                let activityid;
                // let str = e.target.closest('.uncolored-heart').dataset.id 
                // strlen = str.length - 9
                
                // activityid = str.substring(0, strlen)
                activityid = data.id;
                activity_caption = document.getElementById('caption').value;
                editpost(activityid, activity_caption, caption)
                document.querySelector(`.post-view-body`).classList.remove('hide')
                document.querySelector(`.editpost-form`).classList.remove('show')
            }
        })
           
    })
}

function likepost(activityid, nolikes) {
    fetch("/like/"+activityid, {
        method: 'PUT',
        body: JSON.stringify({
            activity_id: activityid
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        return getlike(activityid, nolikes)
    })
}


function editpost(activityid, activity_caption, caption) {
    fetch("/edit/"+activityid, {
        method: 'PUT',
        body: JSON.stringify({
            activity_id: activityid,
            activity_caption: activity_caption
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        return getpost(activityid, caption)
    })
}

function getpost(activityid, caption) {
    fetch("/edit/"+activityid)
    .then(response => response.json())
    .then(data => {
        caption.innerHTML = data.activity;
    })
}

function getlike(activityid, nolikes) {
    fetch("/like/"+activityid)
    .then(response => response.json())
    .then(data => {
        console.log(data.likes)
        // document.querySelector(`#like${activityid}`).innerHTML = data.likes
        nolikes.innerHTML = data.likes
    })
}

function checklike(activityid, color, uncolor) {
    fetch("/isliked/"+activityid)
    .then(response => response.json())
    .then(data => {
        console.log(data.liked)
        if (data.liked == true) {
            uncolor.classList.add('hide')
            color.classList.add('show-inline')
        } 
    })
}
