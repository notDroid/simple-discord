interface LoadingScreenProps {
  /**
   * Optional message to display below the spinner
   */
  message?: string;
  /**
   * Size of the spinner
   * @default "medium"
   */
  size?: 'small' | 'medium' | 'large';
  /**
   * If true, background is slightly transparent with a blur effect
   * useful if loading over existing content.
   */
  blur?: boolean;
  /**
   * Custom class names for the container
   */
  className?: string;
}

export default function LoadingScreen({ 
  message = "Loading...", 
  size = 'medium', 
  blur = false,
  className = ""
}: LoadingScreenProps) {
  
  // Size mapping using standard Tailwind spacing utilities
  const sizeClasses = {
    small: "h-6 w-6 border-2",
    medium: "h-12 w-12 border-4",
    large: "h-16 w-16 border-4",
  };

  return (
    <div 
      role="status"
      aria-live="polite"
      className={`
        fixed inset-0 z-50 flex flex-col items-center justify-center
        transition-opacity duration-300
        ${blur ? 'bg-app-bg/80 backdrop-blur-sm' : 'bg-app-bg'}
        ${className}
      `}
    >
      {/* Animation Container */}
      <div className="relative flex items-center justify-center">
        {/* Outer Ring (Static) - Uses your '--color-app-loading' */}
        <div 
          className={`
            rounded-full border-app-loading
            ${sizeClasses[size]}
          `} 
        />
        
        {/* Inner Spinner (Animated) - Uses your '--color-brand' */}
        <div 
          className={`
            absolute animate-spin rounded-full border-t-brand border-r-transparent border-b-transparent border-l-transparent
            ${sizeClasses[size]}
          `} 
        />
      </div>

      {/* Loading Text */}
      {message && (
        <p className="mt-4 animate-pulse text-sm font-medium text-app-muted">
          {message}
        </p>
      )}
      
      {/* Screen Reader Only */}
      <span className="sr-only">{message}</span>
    </div>
  );
}