document.addEventListener("click", function(event) {
    if(event.target.id === 'btn_1' || event.target.id === 'btn_2' || event.target.id === 'btn_3') {
      event.target.classList.add('active');
    }
  });
  