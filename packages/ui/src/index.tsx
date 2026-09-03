import type { ComponentPropsWithoutRef, ReactNode } from 'react';

const cx = (...parts: Array<string | false | null | undefined>) => parts.filter(Boolean).join(' ');

/* Toolbar: sticky header with title, controls, and a right-aligned status slot. */
export function Toolbar({ title, status, className, children, ...rest }: ComponentPropsWithoutRef<'header'> & { title: string; status?: ReactNode }) {
  return (
    <header className={cx('as-toolbar', className)} {...rest}>
      <h1 className="as-toolbar__title">{title}</h1>
      {children}
      {status !== undefined && <div className="as-status">{status}</div>}
    </header>
  );
}

/* Select: labelled native select. Native because keyboard and screen readers already work. */
export function Select({ label, className, children, ...rest }: ComponentPropsWithoutRef<'select'> & { label: string }) {
  return (
    <label className="as-field">
      {label}
      <select className={cx('as-select', className)} {...rest}>{children}</select>
    </label>
  );
}

/* Toggle: labelled checkbox. */
export function Toggle({ label, className, ...rest }: Omit<ComponentPropsWithoutRef<'input'>, 'type'> & { label: string }) {
  return (
    <label className={cx('as-field', className)}>
      <input type="checkbox" {...rest} /> {label}
    </label>
  );
}

/* Pill: small metadata chip. */
export function Pill({ className, ...rest }: ComponentPropsWithoutRef<'span'>) {
  return <span className={cx('as-pill', className)} {...rest} />;
}

export type Tone = 1 | 2 | 3 | 'danger';

/* Bubble: one chat-style row. Actor column on the left, body on the right. `tone` picks the accent. */
export function Bubble({ from, to, ts, tone = 2, meta, text, className, children, ...rest }: ComponentPropsWithoutRef<'div'> & {
  from: string; to?: string; ts?: string; tone?: Tone; meta?: ReactNode; text?: ReactNode;
}) {
  return (
    <div className={cx('as-bubble', `as-bubble--${tone}`, className)} {...rest}>
      <div className="as-bubble__who">
        <span className="as-bubble__from">{from}</span>
        {ts && <span className="as-bubble__ts">{ts}</span>}
      </div>
      <div>
        {(meta || to) && (
          <div className="as-bubble__head">
            {meta}
            {to && <span className="as-bubble__to">to {to}</span>}
          </div>
        )}
        {text !== undefined && <div className="as-bubble__text">{text}</div>}
        {children}
      </div>
    </div>
  );
}

/* CodeBlock: pre-wrapped monospace, scroll-capped so one long file does not swallow the page. */
export function CodeBlock({ className, ...rest }: ComponentPropsWithoutRef<'pre'>) {
  return <pre className={cx('as-code', className)} {...rest} />;
}

/* Disclosure: <details> with a muted summary. */
export function Disclosure({ summary, className, children, ...rest }: ComponentPropsWithoutRef<'details'> & { summary: ReactNode }) {
  return (
    <details className={cx('as-disclosure', className)} {...rest}>
      <summary>{summary}</summary>
      {children}
    </details>
  );
}

/* Empty: centred muted message. Say what would fill it. */
export function Empty({ className, ...rest }: ComponentPropsWithoutRef<'div'>) {
  return <div className={cx('as-empty', className)} {...rest} />;
}
