document.addEventListener('DOMContentLoaded', function () {
    const collegeDropdown = document.getElementById('college-dropdown');
    const buildingList = document.getElementById('building-list');

    collegeDropdown.addEventListener('change', function () {
        const collegeId = this.value;

        if (collegeId) {
            // Fetch college details to get the shortname
            fetch(`/api/college/${collegeId}`)
                .then(response => response.json())
                .then(collegeData => {
                    const collegeShortname = collegeData.shortname;

                    // Now fetch the buildings for the selected college
                    return fetch(`/api/buildings/${collegeId}`)
                        .then(response => response.json())
                        .then(data => {
                            buildingList.innerHTML = ''; // Clear previous results
                            
                            if (data.buildings.length > 0) {
                                // Create the h3 element
                                const h3 = document.createElement('h3');
                                h3.textContent = `Buildings for ${collegeShortname}`;
                                h3.classList.add('fade-in');  // Add the class for fading in
                                buildingList.appendChild(h3);  // Add the heading to the DOM

                                const ul = document.createElement('ul');
                                ul.classList.add('fade-in'); // Add class for smooth appearance

                                data.buildings.forEach(building => {
                                    const li = document.createElement('li');
                                    li.innerHTML = `<a href="/building/${building.id}/">${building.shortname}</a>`;
                                    ul.appendChild(li);
                                });

                                buildingList.appendChild(ul);

                                // Trigger fade-in animation after building list is appended
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
            buildingList.innerHTML = ''; // Clear when no college is selected
        }
    });
});
