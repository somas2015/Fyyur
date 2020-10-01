window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};



function createVenue() {
  alert("hello")
  
  fetch('/venues/create', {
    method: 'POST',
    body: JSON.stringify({
       'name': document.getElementById("form").name.value,
       'city': document.getElementById("form").city.value,
       'state': document.getElementById("form").state.value,
       'address': document.getElementById("form").address.value,
       'phone': document.getElementById("form").phone.value,
       'image_link': document.getElementById("form").image_link.value,
       'facebook_link': document.getElementById("form").facebook_link.value

    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(function (response) {
      return response.json();
    })
    .catch(function () {
      console.log('has-error');
    }).finally(function () {
      render('/venues/create');
    });

}

function createArtist() {
  // alert("hello");
  fetch('/artists/create', {
    method: 'POST',
    body: JSON.stringify({
       'name': document.getElementById("form").name.value,
       'city': document.getElementById("form").city.value,
       'state': document.getElementById("form").state.value,
       'phone': document.getElementById("form").phone.value,
	     'genres' : document.getElementById("form").genres.value,
       'image_link': document.getElementById("form").image_link.value,
       'facebook_link': document.getElementById("form").facebook_link.value

    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(function (response) {
      return response.json();
    })
    .catch(function () {
      console.log('has-error');
    })

}


function createShow(){
  
  fetch('/shows/create',{
    method : 'POST',
    body : JSON.stringify({
      'artist_id' : document.getElementById("form").artist_id.value,
      'venue_id' : document.getElementById("form").venue_id.value,
      'start_time' : document.getElementById("form").start_time.value
    }),
    headers: {
      'Content-Type' : 'application/json'
    }
  })
  .then(function(response){
    return response.json();
  })
  .catch(function(){
    console.log('has-error');
  })
}




function deleteBtn(){
  
  venueId = document.getElementById('delete-button').getAttribute('data-id');
   
  fetch('/venues/'+venueId,{
    method:'DELETE',
    headers: {
    'Content-Type': 'application/json'
  }
})
 .then(
    alert("Successfully removed!")
  ).catch(function() {
    console.log('has error')
  });
}

function editArtistBtn(){
  artistId = document.getElementById('artist-edit-button').getAttribute('data-id');
  fetch('/artists/'+artistId+'/edit', {
    method: 'POST',
    body: JSON.stringify({
       'name': document.getElementById("form").name.value,
       'city': document.getElementById("form").city.value,
       'state': document.getElementById("form").state.value,
       'phone': document.getElementById("form").phone.value,
	     'genres' : document.getElementById("form").genres.value,
       'image_link': document.getElementById("form").image_link.value,
       'facebook_link': document.getElementById("form").facebook_link.value

    }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
}

function editVenueBtn(){
  venueId = document.getElementById('edit-button-venue').getAttribute('data-id');
  fetch('/venues/'+venueId+'/edit', {
    method: 'POST',
    body: JSON.stringify({
       'name': document.getElementById("form").name.value,
       'city': document.getElementById("form").city.value,
       'state': document.getElementById("form").state.value,
       'address': document.getElementById("form").address.value,
       'phone': document.getElementById("form").phone.value,
       'seeking_talent': document.getElementById("form").seeking_talent.checked, 
       'seeking_description': document.getElementById("form").seeking_description.value,
	     'image_link': document.getElementById("form").image_link.value,
       'facebook_link': document.getElementById("form").facebook_link.value

    }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
}