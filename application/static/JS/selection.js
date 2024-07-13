document.addEventListener('DOMContentLoaded', (event) => {
    const selectElement = document.getElementById('selectDateInterval');
    
    selectElement.addEventListener('change', (event) => {
        const selectedOption = event.target.value;
        if(selectedOption === "select_time_interval")
        {
            showSetInterval();
        }
        else
        {
            triggerRequest(event.target.value);
            hideSetInterval();
        }
    });
    
    const showSetInterval = () => {
        const intervalSection = document.getElementById("setDateTimeInterval");
        intervalSection.style.visibility = "visible";
    };
    const hideSetInterval = () => {
        const intervalSection = document.getElementById("setDateTimeInterval");
        intervalSection.style.visibility = "hidden";
    };
    const triggerRequest = (interval) => {
        const dateSetStart = document.getElementById('start-date');
        const dateSetEnd = document.getElementById('end-date');
        dateSetStart.value = '';
        dateSetEnd.value = '';
    };
});
