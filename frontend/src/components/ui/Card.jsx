export const Card = ({ children }) => (
  <div className="rounded-lg border shadow-md p-4 bg-white">
    {children}
  </div>
);

export const CardHeader = ({ children }) => (
  <div className="border-b pb-2 mb-4">
    {children}
  </div>
);

export const CardTitle = ({ children }) => (
  <h2 className="text-xl font-bold">{children}</h2>
);

export const CardContent = ({ children }) => (
  <div>{children}</div>
);
