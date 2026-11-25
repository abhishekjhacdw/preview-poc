import { NavLink } from 'react-router-dom';
import { routes } from '../../routes/index.jsx';

const patientRoutes = routes.filter((route) => route.group === 'Patient');
const staffRoutes = routes.filter((route) => route.group === 'Staff');

export function AppLayout({ children }) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="brand-kicker">Clinic Booking</p>
          <h1>Scheduling Workspace</h1>
        </div>
        <div className="status-pill">No patient login required</div>
      </header>

      <div className="workspace">
        <aside className="sidebar" aria-label="Primary navigation">
          <NavGroup title="Patient" routes={patientRoutes} />
          <NavGroup title="Staff" routes={staffRoutes} />
        </aside>
        <main className="content" tabIndex="-1">
          {children}
        </main>
      </div>
    </div>
  );
}

function NavGroup({ title, routes: groupRoutes }) {
  return (
    <section className="nav-group">
      <h2>{title}</h2>
      <nav>
        {groupRoutes.map((route) => {
          const Icon = route.icon;

          return (
            <NavLink
              key={route.path}
              to={route.path}
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            >
              <Icon aria-hidden="true" size={18} strokeWidth={2} />
              <span>{route.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </section>
  );
}
