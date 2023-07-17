// document.addEventListener('DOMContentLoaded', function() {
//     const serviceButton = document.getElementById('serviceButton');
//     const serviceNameInput = document.getElementById('serviceNameInput');
//     const userNameInput = document.getElementById('userNameInput');
//     const userNames = ['Steam', 'Kakao'];
//     let currentIndex = 0;

//     serviceButton.addEventListener('click', function() {
//         currentIndex = (currentIndex + 1) % userNames.length;
//         const serviceName = userNames[currentIndex];
//         serviceButton.textContent = serviceName;
//         serviceNameInput.value = serviceName.toLowerCase();
//         checkInputValidity();
//     });

//     userNameInput.addEventListener('input', function() {
//         checkInputValidity();
//     });

//     function checkInputValidity() {
//         if (userNameInput.value.trim() === '') {
//             document.getElementById('searchButton').disabled = true;
//         } else {
//             document.getElementById('searchButton').disabled = false;
//         }
//     }

//     checkInputValidity();
// });

document.addEventListener('DOMContentLoaded', function() {
    const serviceButton = document.getElementById('serviceButton');
    const serviceNameInput = document.getElementById('serviceNameInput');
    const userNameInput = document.getElementById('userNameInput');
    const userNames = ['Steam', 'Kakao'];
    let currentIndex = 0;
    const searchButton = document.getElementById('searchButton');

    serviceButton.addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % userNames.length;
        const serviceName = userNames[currentIndex];
        serviceButton.textContent = serviceName;
        serviceNameInput.value = serviceName.toLowerCase();
        checkInputValidity();
    });

    userNameInput.addEventListener('input', function() {
        checkInputValidity();
    });

    function checkInputValidity() {
        if (userNameInput.value.trim() === '') {
            searchButton.disabled = true;
        } else {
            searchButton.disabled = false;
        }
    }

    checkInputValidity();
});