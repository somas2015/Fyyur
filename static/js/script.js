window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};


if (document.getElementById("venue-form") != null){
  document.getElementById("venue-form").addEventListener('submit', function(e){
  e.preventDefault();
  var fyyur_success = false;
  fetch('/venues/create', {
        method: 'POST',
        body: JSON.stringify({
           'name': document.getElementById("venue-form").name.value,
           'city': document.getElementById("venue-form").city.value,
           'state': document.getElementById("venue-form").state.value,
           'address': document.getElementById("venue-form").address.value,
           'phone': document.getElementById("venue-form").phone.value,
           'image_link': document.getElementById("venue-form").image_link.value,
           'facebook_link': document.getElementById("venue-form").facebook_link.value
    
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(function (response) {
        fyyur_success = true;
        return response.json();
      })
      .catch(function () {
        console.log('has-error');
      }).finally(function () {
        console.log('Venue created');
        if(fyyur_success){
          window.location.href ='/venues';
        }
                 
      });
    
});
}


if (document.getElementById("venue-form-edit") != null){
document.getElementById('venue-form-edit').addEventListener('submit',function(e){
  var fyyur_success = false;
  e.preventDefault();
  venueId = document.getElementById('edit-button-venue').getAttribute('data-id');
  // document.getElementById('venue-form-edit')=form;
  fetch('/venues/'+venueId+'/edit', {
    method: 'POST',
    body: JSON.stringify({
       'name': document.getElementById('venue-form-edit').name.value,
       'city': document.getElementById('venue-form-edit').city.value,
       'state': document.getElementById('venue-form-edit').state.value,
       'address': document.getElementById('venue-form-edit').address.value,
       'phone': document.getElementById('venue-form-edit').phone.value,
       'seeking_talent': document.getElementById('venue-form-edit').seeking_talent.checked, 
       'seeking_description': document.getElementById('venue-form-edit').seeking_description.value,
	     'image_link': document.getElementById('venue-form-edit').image_link.value,
       'facebook_link': document.getElementById('venue-form-edit').facebook_link.value

    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function (response) {
    fyyur_success = true;
    return response.json();
  })
  .finally(function(){
    if(fyyur_success){
      window.location.href ='/venues';
    }
    
  });

});
}

if (document.getElementById("artist-form") != null){
  document.getElementById("artist-form").addEventListener('submit', function(e){
    var fyyur_success = false;
    e.preventDefault();
    fetch('/artists/create', {
      method: 'POST',
      body: JSON.stringify({
         'name': document.getElementById("artist-form").name.value,
      
         'city': document.getElementById("artist-form").city.value,
         'state': document.getElementById("artist-form").state.value,
         'phone': document.getElementById("artist-form").phone.value,
         'genres' : document.getElementById("artist-form").genres.value,
         'image_link': document.getElementById("artist-form").image_link.value,
         'facebook_link': document.getElementById("artist-form").facebook_link.value
  
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(function (response) {
       fyyur_success = true;
        return response.json();
      })
      .catch(function () {
        console.log('has-error');
      })
      .finally(function(){
        if(fyyur_success){
          window.location.href ='/artists';
        }
        
      })
  
  });
}

if (document.getElementById("artist-form-edit") != null){
  document.getElementById("artist-form-edit").addEventListener('submit', function(e){
    e.preventDefault();
    var fyyur_success = false;
    artistId = document.getElementById('edit-button-artist').getAttribute('data-id');
    fetch('/artists/'+artistId+'/edit', {
      method: 'POST',
       body: JSON.stringify({
        'name': document.getElementById("artist-form-edit").name.value,
        'city': document.getElementById("artist-form-edit").city.value,
        'state': document.getElementById("artist-form-edit").state.value,
        'phone': document.getElementById("artist-form-edit").phone.value,
        'genres' : document.getElementById("artist-form-edit").genres.value,
        'image_link': document.getElementById("artist-form-edit").image_link.value,
        'facebook_link': document.getElementById("artist-form-edit").facebook_link.value

      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function (response) {
      fyyur_success = true;
      return response.json();
    })
    .finally(function(){
      if(fyyur_success){
        window.location.href ='/artists';
      }
    }) 
  });
}

if (document.getElementById("show-form") != null){
  document.getElementById("show-form").addEventListener('submit', function(e){
    var fyyur_success = false;
    e.preventDefault();
    fetch('/shows/create',{
      method : 'POST',
      body : JSON.stringify({
        'artist_id' : document.getElementById("show-form").artist_id.value,
        'venue_id' : document.getElementById("show-form").venue_id.value,
        'start_time' : document.getElementById("show-form").start_time.value
      }),
      headers: {
        'Content-Type' : 'application/json'
      }
    })
    .then(function(response){
      fyyur_success = true;
      return response.json();
    })
    .catch(function(){
      console.log('has-error');
    })
    .finally(function(){
      if(fyyur_success){
        window.location.href ='/shows';
      }
    }) 
  
  }); 
}



function deleteBtn(){
  
  venueId = document.getElementById('venue-delete-button').getAttribute('data-id');
   
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





