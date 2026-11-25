import {
  CalendarClock,
  ClipboardCheck,
  ClipboardList,
  Repeat2,
  Settings2
} from 'lucide-react';
import { PlaceholderView } from '../components/layout/PlaceholderView.jsx';
import { BookingPage } from '../pages/BookingPage.jsx';

export const routes = [
  {
    path: '/book',
    label: 'Book',
    group: 'Patient',
    icon: CalendarClock,
    element: <BookingPage />
  },
  {
    path: '/reschedule',
    label: 'Reschedule',
    group: 'Patient',
    icon: Repeat2,
    element: (
      <PlaceholderView
        title="Reschedule Appointment"
        eyebrow="Patient workflow"
        description="A public rescheduling flow placeholder for changing an existing appointment using appointment reference details."
        actions={['Find appointment', 'Review alternatives', 'Confirm change']}
      />
    )
  },
  {
    path: '/staff/schedule',
    label: 'Schedule',
    group: 'Staff',
    icon: ClipboardList,
    element: (
      <PlaceholderView
        title="Staff Schedule"
        eyebrow="Staff workflow"
        description="A staff schedule placeholder for viewing daily clinic capacity, appointments, and availability."
        actions={['Review daily schedule', 'Inspect appointment details', 'Coordinate provider availability']}
      />
    )
  },
  {
    path: '/staff/requests',
    label: 'Requests',
    group: 'Staff',
    icon: ClipboardCheck,
    element: (
      <PlaceholderView
        title="Request Review"
        eyebrow="Staff workflow"
        description="A staff review placeholder for triaging booking and rescheduling requests that need manual action."
        actions={['Prioritize incoming requests', 'Approve or decline changes', 'Record review outcome']}
      />
    )
  },
  {
    path: '/staff/appointment-types',
    label: 'Types',
    group: 'Staff',
    icon: Settings2,
    element: (
      <PlaceholderView
        title="Appointment Type Controls"
        eyebrow="Staff workflow"
        description="A controls placeholder for managing visit types, durations, availability rules, and intake requirements."
        actions={['Maintain appointment types', 'Set scheduling rules', 'Adjust patient-facing availability']}
      />
    )
  }
];
