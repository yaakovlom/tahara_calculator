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
    const deleteEventButton = document.getElementById('delete-event');
    const eventDateInput = document.getElementById('event-date');
    const eventNoteInput = document.getElementById('event-note');
    const eventTypeInput = document.getElementById('event-type');
    const eventDayTimeInput = document.getElementById('event-daytime');
    const eventIdInput = document.getElementById('event-id');

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
            days += `<div class="prev-date" data-date="${dateToISO(prevDate)}"><span>${prevLastDay - x + 1}</span></div>`;
        }

        for (let i = 1; i <= lastDay; i++) {
            const currentDate = new Date(year, month, i + 1);
            const dateKey = dateToISO(currentDate);
            
            // create night events
            const nightEventsList = events[dateKey] ? events[dateKey].filter(event => event.dayTime === 'night') : [];
            const nightEventElements = nightEventsList.map(event => `<button class="event ${event.type}" id="${event.id}" title="${event.note}"></button>`).join('');

            // create day events
            const dayEventsList = events[dateKey] ? events[dateKey].filter(event => event.dayTime === 'day') : [];
            const dayEventElements = dayEventsList.map(event => `<button class="event ${event.type}" id="${event.id}" title="${event.note}"></button>`).join('');

            // create events box
            const eventsBox = `<span class="eventsBox"><span class="eventsBox night">${nightEventElements}</span><span class="eventsBox day">${dayEventElements}</span></span>`;

            if (
                i === new Date().getDate() &&
                year === new Date().getFullYear() &&
                month === new Date().getMonth()
            ) {
                days += `<div class="today" data-date="${dateKey}"><span>${getHebDay(date)} / ${i}</span>${eventsBox}</div>`;
            } else {
                days += `<div data-date="${dateKey}"><span>${getHebDay(new Date(year, month, i))} / ${i}</span>${eventsBox}</div>`;
            }
        }

        for (let j = 1; j <= nextDays; j++) {
            const nextDate = new Date(year, month + 1, j + 1);
            days += `<div class="next-date" data-date="${dateToISO(nextDate)}"><span>${j}</span></div>`;
        }
        daysContainer.innerHTML = days;

        // Add event listeners to each date cell
        document.querySelectorAll('.days div').forEach(day => {
            day.addEventListener('click', handleDateClick);
        });

        // Add event listeners to each event button
        document.querySelectorAll('.event').forEach(event => {
            event.addEventListener('click', handleEventClick);
        });
    };

    //// ------------------ Event Handlers ------------------ ////

    const handleDateClick = (event) => {
        if(event.target.type === 'submit') return;
        const target = event.target.closest('div');
        const date = target.dataset.date;
        openEventModal(date);
    };

    const handleEventClick = (event) => {
        const target = event.target.closest('button');
        const eventId = target.id;
        const eventDate = target.parentElement.parentElement.parentElement.dataset.date;
        const eventNote = target.title;
        const eventType = target.classList[1];
        const eventDayTime = target.parentElement.classList[1];

        openEventModal(eventDate, eventType, eventDayTime, eventNote, eventId);
    };
    
    const openEventModal = (eventDate, eventType, eventDayTime, eventNote, eventId) => {
        eventModal.style.display = 'block';
        eventDateInput.value = eventDate;
        eventTypeInput.value = eventType || "menstrual";
        eventDayTimeInput.value = eventDayTime || "day";
        eventNoteInput.value = eventNote || '';
        eventIdInput.value = eventId || '';
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
        openEventModal();
    });

    closeModal.addEventListener('click', () => {
        eventModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === eventModal) {
            eventModal.style.display = 'none';
        }
    });

    saveEventButton.addEventListener('click', async () => {
        const eventDate = eventDateInput.value;
        const eventNote = eventNoteInput.value;
        const eventId = eventIdInput.value || null;
        const eventType = eventTypeInput.value || "menstrual";
        const eventDayTime = eventDayTimeInput.value || "day";

        const existingEvent = events[eventDate] ? events[eventDate].find(event => event.type === eventType && event.dayTime === eventDayTime && eventId === null) : null;
        if (existingEvent) {
            alert(`אירוע כבר קיים בתאריך זה`);
            clearModel();
            return;
        }

        if (eventDate) {
            // console.log(eventDate, eventType, eventDayTime, eventNote, eventId);
            const newEvent = {id: eventId, type: eventType, dayTime: eventDayTime, note: eventNote};
            updateEvent(eventDate, newEvent, eventId ? "update" : "add");
            clearModel();
        }
    });

    deleteEventButton.addEventListener('click', async () => {
        const eventId = eventIdInput.value;
        const eventDate = eventDateInput.value;
        console.log(eventId);
        if (eventId) {
            const response = await fetch('/api/events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ flag: "delete", date: eventDate, event: {id: eventId} })
            })
    
            if (!response.ok) {
                throw new Error('Failed to delete event from the server');
            }
        
            clearModel();
            return fetchEventsFromServer();
        }
    });

    const clearModel = () => {
        eventDateInput.value = '';
        eventNoteInput.value = '';
        eventTypeInput.value = "menstrual";
        eventDayTimeInput.value = "day";
        eventModal.style.display = 'none';
    };

    async function fetchEventsFromServer() {
        const response = await fetch('/api/events');
        if (!response.ok) {
            throw new Error('Failed to fetch events from the server');
        }
        events = await response.json();
        renderCalendar(currentDate);
    }

    async function updateEvent(eventDate, event, flag) {
        const response = await fetch('/api/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ flag: flag, date: eventDate, event: event })
        })

        if (!response.ok) {
            throw new Error('Failed to send new event to the server');
        }
    
        return fetchEventsFromServer();
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

    fetchEventsFromServer();
});
