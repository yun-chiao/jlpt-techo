import { useEffect } from 'react';
import { SITE_NAME, SITE_NAME_EN } from '../data/meta';

/** 動態設定 <title>；傳入頁面標題，自動附上站名。 */
export function useDocumentTitle(pageTitle?: string): void {
  useEffect(() => {
    document.title = pageTitle ? `${pageTitle}｜${SITE_NAME}` : `${SITE_NAME} ${SITE_NAME_EN}｜JLPT 自學網站`;
  }, [pageTitle]);
}
