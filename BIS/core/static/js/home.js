document.addEventListener('DOMContentLoaded', function () {
    const collegeDropdown = document.getElementById('college-dropdown');
    const buildingList = document.getElementById('building-list');

    collegeDropdown.addEventListener('change', function () {
        const collegeId = this.value;

        if (collegeId) {
            fetch(`/api/college/${collegeId}`)
                .then(response => response.json())
                .then(collegeData => {
                    const collegeShortname = collegeData.shortname;

                    return fetch(`/api/buildings/${collegeId}`)
                        .then(response => response.json())
                        .then(data => {
                            buildingList.innerHTML = ''; 
                            
                            if (data.buildings.length > 0) {
                                const h3 = document.createElement('h3');
                                h3.textContent = `Buildings for ${collegeShortname}`;
                                h3.classList.add('fade-in');  
                                buildingList.appendChild(h3); 

                                const ul = document.createElement('ul');
                                ul.classList.add('fade-in');

                                data.buildings.forEach(building => {
                                    const li = document.createElement('li');
                                    li.innerHTML = `<a href="/building/${building.id}/">${building.shortname}</a>`;
                                    ul.appendChild(li);
                                });

                                buildingList.appendChild(ul);

                                setTimeout(() => {
                                    h3.classList.add('show');
                                    ul.classList.add('show');
                                }, 10);
                            } else {
                                buildingList.textContent = 'No buildings found.';
                            }
                        });
                })
                .catch(error => console.error('Error:', error));
        } else {
            buildingList.innerHTML = '';
        }
    });
});
