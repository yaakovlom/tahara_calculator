document.addEventListener('DOMContentLoaded', () => {
    const monthYear = document.getElementById('month-year');
    const hebrewMonthYear = document.getElementById('hebrew-month-year');
    const daysContainer = document.getElementById('days');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    const todayButton = document.getElementById('today');
    const gotoButton = document.getElementById('goto-button');
    const gotoDateInput = document.getElementById('goto-date');
    const addEventButton = document.getElementById('add-event');
    const eventModal = document.getElementById('event-modal');
    const closeModal = document.querySelector('.close');
    const saveEventButton = document.getElementById('save-event');
    const eventDateInput = document.getElementById('event-date');
    const eventNoteInput = document.getElementById('event-note');

    let currentDate = new Date();
    let events = {};

    const renderCalendar = (date) => {
        date.setDate(1);
        const month = date.getMonth();
        const year = date.getFullYear();

        const firstDayIndex = date.getDay();
        const lastDay = new Date(year, month + 1, 0).getDate();
        const prevLastDay = new Date(year, month, 0).getDate();

        const nextDays = 7 - new Date(year, month + 1, 0).getDay() - 1;

        const months = [
            "ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני",
            "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"
        ];

        monthYear.innerText = `${months[month]} ${year}`;
        hebrewMonthYear.innerText = getHebHeader(date);

        const dateToISO = (date) => {
            return date.toISOString().split('T')[0];
        };
        
        let days = "";

        for (let x = firstDayIndex; x > 0; x--) {
            const prevDate = new Date(year, month - 1, prevLastDay - x + 2);
            days += `<div class="prev-date" data-date="${dateToISO(prevDate)}">${prevLastDay - x + 1}</div>`;
        }

        for (let i = 1; i <= lastDay; i++) {
            const currentDate = new Date(year, month, i + 1);
            const eventKey = dateToISO(currentDate);
            const event = events[eventKey] && events[eventKey].note ? `<div class="event">${events[eventKey].note}</div>` : '';
            if (
                i === new Date().getDate() &&
                year === new Date().getFullYear() &&
                month === new Date().getMonth()
            ) {
                days += `<div class="today" data-date="${eventKey}">${getHebDay(date)} / ${i}${event}</div>`;
            } else {
                days += `<div data-date="${eventKey}">${getHebDay(new Date(year, month, i))} / ${i}${event}</div>`;
            }
        }

        for (let j = 1; j <= nextDays; j++) {
            const nextDate = new Date(year, month + 1, j + 1);
            days += `<div class="next-date" data-date="${dateToISO(nextDate)}">${j}</div>`;
        }
        daysContainer.innerHTML = days;

        // Add event listeners to each date cell
        document.querySelectorAll('.days div').forEach(day => {
        day.addEventListener('click', handleDateClick);
    });
    };

    //// ------------------ Event Handlers ------------------ ////

    const handleDateClick = (event) => {
        const target = event.target;
        const date = target.dataset.date;
        openAddEventModal(date);
    };
    
    const openAddEventModal = (date) => {
        eventModal.style.display = 'block';
        eventDateInput.value = date;
    };
    
    prevButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    todayButton.addEventListener('click', () => {
        currentDate = new Date();
        renderCalendar(currentDate);
    });

    gotoButton.addEventListener('click', () => {
        const selectedDate = new Date(gotoDateInput.value);
        if (!isNaN(selectedDate)) {
            currentDate = selectedDate;
            renderCalendar(currentDate);
        }
    });

    addEventButton.addEventListener('click', () => {
        eventModal.style.display = 'block';
    });

    closeModal.addEventListener('click', () => {
        eventModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === eventModal) {
            eventModal.style.display = 'none';
        }
    });

    saveEventButton.addEventListener('click', () => {
        const eventDate = eventDateInput.value;
        const eventNote = eventNoteInput.value;
        const eventType = document.getElementById('event-type').value || "מחזור";

        if (eventDate) {
            events[eventDate] = { note: eventNote, type: eventType };
            renderCalendar(currentDate);
            eventDateInput.value = '';
            eventNoteInput.value = '';
            document.getElementById('event-type').value = "מחזור";
            eventModal.style.display = 'none';
            saveEvents();
        }
    });

    const saveEvents = () => {
        fetch('/api/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(events)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => console.error('Error saving events:', error));
        console.log('Saving events:', events);
    };

    //// ------------------ Hebrew Calendar ------------------ ////

    const toHebCount = (n) => {
        const thousands = 'ת'.repeat(Math.floor(n / 400));
        const hundreds = "קרש"[Math.floor(n % 400 / 100) - 1] ?? [];
        const tens = "יכלמנסעפצ"[Math.floor(n % 100 / 10) - 1] ?? [];
        const ones = "אבגדהוזחט"[n % 10 - 1] ?? [];
        const specialCases = n % 100 === 15 ? ['טו'] : n % 100 === 16 ? ['טז'] : [];
        hebCount = specialCases.length > 0 
            ? [...thousands, ...hundreds, ...specialCases] 
            : [...thousands, ...hundreds, ...specialCases, ...tens, ...ones];
        if (hundreds.length > 0) {
            hebCount = hebCount.toSpliced(-1,0, '"');
        }
        return hebCount.join('');
    };

    const getHebYear = (date) => {
        const getX = opt => Intl.DateTimeFormat('he-u-ca-hebrew', { [opt]: 'numeric' }).format(date || new Date());
        return toHebCount(getX('year') % 1e3);
    }

    const getHebMonth = (date) => {
        const getX = opt => Intl.DateTimeFormat('he-u-ca-hebrew', { [opt]: 'numeric' }).format(date || new Date());
        return getX('month');
    }

    const getHebDay = (date) => {
        const getX = opt => Intl.DateTimeFormat('he-u-ca-hebrew', { [opt]: 'numeric' }).format(date || new Date());
        return toHebCount(getX('day'));
    }

    const getHebHeader = (date) => {
        const month = getHebMonth(new Date(date.getFullYear(), date.getMonth(), 1));
        const nextMonth = getHebMonth(new Date(date.getFullYear(), date.getMonth() + 1, 0));
        const year = getHebYear(date);
        const header = month === nextMonth ? `${month} ${year}` : `${month}-${nextMonth} ${year}`;
        return header
    };

    fetch('/api/events')
        .then(response => response.json())
        .then(data => {
            events = data;
            renderCalendar(currentDate);
        })
        .catch(error => console.error('Error loading events:', error));

    renderCalendar(currentDate);
});
