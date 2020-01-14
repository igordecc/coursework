import usePersistentCanvas from './usePersistentCanvas';
import usePersistentData from './usePersistentData';

export default function useAllData() {
    const [data, setData] = usePersistentData({});
    const [locations, setLocations, zipped, colorList, setColorList, screenLines, setScreenLines] = usePersistentCanvas(data);

    return {
        'data': data,
        'setData': setData,
        'locations': locations,
        'setLocations': setLocations,
        'zipped': zipped,
        'colorList': colorList,
        'setColorList': setColorList,
        'screenLines': screenLines,
        'setScreenLines':setScreenLines,
        
    }
}