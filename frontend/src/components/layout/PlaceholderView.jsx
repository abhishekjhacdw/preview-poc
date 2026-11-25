export function PlaceholderView({ title, eyebrow, description, actions }) {
  return (
    <section className="placeholder-view" aria-labelledby={`${slugify(title)}-title`}>
      <div className="placeholder-heading">
        <p>{eyebrow}</p>
        <h2 id={`${slugify(title)}-title`}>{title}</h2>
        <span>Ready for feature implementation</span>
      </div>
      <p className="placeholder-description">{description}</p>
      <div className="placeholder-actions" aria-label="Workflow outline">
        {actions.map((action, index) => (
          <article className="workflow-step" key={action}>
            <strong>{String(index + 1).padStart(2, '0')}</strong>
            <span>{action}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}
