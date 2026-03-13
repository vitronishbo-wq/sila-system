export const StatisticsSkeleton = () => (
    <div className="space-y-6 max-w-7xl mx-auto px-4 py-12">
        <div className="h-10 bg-gray-200 rounded-xl w-64 mb-12 skeleton-shimmer"></div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
            {[1, 2, 3, 4].map((i) => (
                <div key={i} className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                    <div className="flex items-center justify-between mb-6">
                        <div className="h-10 w-10 bg-gray-200 rounded-2xl skeleton-shimmer"></div>
                        <div className="h-4 w-4 bg-gray-200 rounded-full skeleton-shimmer"></div>
                    </div>
                    <div className="h-3 bg-gray-200 rounded w-20 mb-3 skeleton-shimmer"></div>
                    <div className="h-10 bg-gray-200 rounded-xl w-24 skeleton-shimmer"></div>
                </div>
            ))}
        </div>

        <div className="bg-white rounded-[3rem] shadow-xl p-10 border border-gray-100 chart-container">
            <div className="h-6 bg-gray-200 rounded w-48 mb-12 skeleton-shimmer"></div>
            <div className="h-[450px] bg-gray-50 rounded-[2rem] skeleton-shimmer"></div>
        </div>
    </div>
);
