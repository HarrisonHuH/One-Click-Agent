/**
 * 通用按钮组件
 */
import React from 'react'
import './Button.css'

type ButtonVariant = 'primary' | 'secondary' | 'gradient' | 'ghost' | 'danger'
type ButtonSize = 'sm' | 'md' | 'lg'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  block?: boolean
  loading?: boolean
  icon?: React.ReactNode
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  block = false,
  loading = false,
  icon,
  children,
  className = '',
  ...rest
}) => {
  const classes = [
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    block && 'btn-block',
    loading && 'btn-loading',
    className
  ].filter(Boolean).join(' ')

  return (
    <button className={classes} disabled={loading || rest.disabled} {...rest}>
      {loading && <span className="btn-spinner" />}
      {!loading && icon && <span className="btn-icon">{icon}</span>}
      {children && <span>{children}</span>}
    </button>
  )
}

export default Button
