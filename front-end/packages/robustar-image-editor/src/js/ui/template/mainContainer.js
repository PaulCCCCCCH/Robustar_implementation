export default ({
  locale,
  biImage,
  commonStyle,
  headerStyle,
  loadButtonStyle,
  downloadButtonStyle,
  submenuStyle,
  replaceDownload,
}) => `
    <div class="tui-image-editor-main-container" style="${commonStyle}">
        <div class="tui-image-editor-header" style="${headerStyle}">
            <!--
            <div class="tui-image-editor-header-logo">
                <img src="${biImage}" />
            </div>
            -->
            <div class="tui-image-editor-header-buttons">
                <!--
                <div ${replaceDownload ? 'hidden' : ''}
                style="${loadButtonStyle}">
                    ${locale.localize('Load')}
                    <input type="file" class="tui-image-editor-load-btn" />
                </div>
                <button class="tui-image-editor-download-btn" 
                ${replaceDownload ? 'hidden' : ''} 
                style="${downloadButtonStyle}">
                    ${locale.localize('Download')}
                </button>
                -->
                <button class="tui-image-editor-adjust-size-btn"
                ${replaceDownload ? '' : 'hidden'} 
                style="${loadButtonStyle}">
                    ${locale.localize('Adjust Size')}
                </button>
                <button class="tui-image-editor-send-edit-btn"
                ${replaceDownload ? '' : 'hidden'} 
                style="${downloadButtonStyle}">
                    ${locale.localize('Send Edit')}
                </button>
            </div>
        </div>
        <div class="tui-image-editor-main">
            <div class="tui-image-editor-submenu">
                <div class="tui-image-editor-submenu-style" style="${submenuStyle}"></div>
            </div>
            <div class="tui-image-editor-wrap">
                <div class="tui-image-editor-size-wrap">
                    <div class="tui-image-editor-align-wrap">
                        <div class="tui-image-editor"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
`;
