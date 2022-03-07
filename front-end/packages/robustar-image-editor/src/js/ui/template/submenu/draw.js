/**
 * @param {Object} submenuInfo - submenu info for make template
 *   @param {Locale} locale - Translate text
 *   @param {Function} makeSvgIcon - svg icon generator
 * @returns {string}
 */
export default ({ locale, makeSvgIcon }) => `
    <ul class="tui-image-editor-submenu-item">
        <li class="tie-draw-line-select-button">
            <div class="tui-image-editor-button free">
                <div>
                    ${makeSvgIcon(['normal', 'active'], 'draw-free', true)}
                </div>
                <label>
                    ${locale.localize('Free')}
                </label>
            </div>

            <!-- line drawing not needed
            <div class="tui-image-editor-button line">
                <div>
                    ${makeSvgIcon(['normal', 'active'], 'draw-line', true)}
                </div>
                <label>
                    ${locale.localize('Straight')}
                </label>
            </div>
            -->
            <div class="tui-image-editor-button color-range">
                <div>
                    ${makeSvgIcon(['normal', 'active'], 'mask', true)}
                </div>
                <label>
                    ${locale.localize('Color Range')}
                </label>
            </div>
        </li>
        <li class="tui-image-editor-partition">
            <div style="display: none">
            <div></div>
            </div>
        </li>
        <li>
            <div style="display: none">
                <div class="tie-draw-color" title="${locale.localize('Color')}"></div>
            </div>
        </li>
        <li class="tui-image-editor-partition only-left-right">
            <div></div>
        </li>
        <li class="tui-image-editor-newline tui-image-editor-range-wrap">
            <label class="range">${locale.localize('Range')}</label>
            <div class="tie-draw-range"></div>
            <input class="tie-draw-range-value tui-image-editor-range-value" value="0" />
        </li>
    </ul>
`;
