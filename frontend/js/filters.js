/**
 * パーツフィルタリング機能
 * 汎用的なフィルタリング機能を提供
 */

class PartsFilter {
  constructor(containerId, data) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.error(`Container element with id '${containerId}' not found`);
      return;
    }
    this.originalData = data;
    this.filteredData = [...data];
    this.filters = {};
    this.filterOptions = {};
    
    this.init();
  }

  init() {
    this.extractFilterOptions();
    this.populateFilterSelects();
    this.attachEventListeners();
  }

  // データからフィルターオプションを抽出
  extractFilterOptions() {
    if (this.originalData.length === 0) return;

    const sample = this.originalData[0];
    
    // メーカー
    if (sample.maker !== undefined) {
      this.filterOptions.maker = [...new Set(this.originalData.map(item => item.maker))].sort();
    }

    // CPUの場合
    if (sample.core !== undefined) {
      this.filterOptions.core = [...new Set(this.originalData.map(item => item.core))].sort((a, b) => a - b);
    }

    // GPUの場合
    if (sample.chipset_id !== undefined && sample.vram !== undefined) {
      this.filterOptions.chipset = [...new Set(this.originalData.map(item => item.chipset_name || item.chipset_id))].sort();
      this.filterOptions.vram = [...new Set(this.originalData.map(item => item.vram))].sort();
    }

    // メモリの場合
    if (sample.capacity_gb !== undefined && sample.speed_mhz !== undefined) {
      this.filterOptions.capacity = [...new Set(this.originalData.map(item => item.capacity_gb))].sort((a, b) => a - b);
      this.filterOptions.speed = [...new Set(this.originalData.map(item => item.speed_mhz))].sort((a, b) => a - b);
    }

    // ストレージの場合
    if (sample.storage_type !== undefined) {
      this.filterOptions.type = [...new Set(this.originalData.map(item => item.storage_type))].sort();
      if (sample.capacity_gb !== undefined) {
        this.filterOptions.capacity = [...new Set(this.originalData.map(item => item.capacity_gb))].sort((a, b) => a - b);
      }
    }

    // マザーボードの場合
    if (sample.socket_type !== undefined && sample.form_factor !== undefined) {
      this.filterOptions.socket = [...new Set(this.originalData.map(item => item.socket_type))].sort();
      this.filterOptions.formFactor = [...new Set(this.originalData.map(item => item.form_factor))].sort();
    }

    // クーラーの場合
    if (sample.cooler_type !== undefined) {
      this.filterOptions.type = [...new Set(this.originalData.map(item => item.cooler_type))].sort();
    }

    // 電源の場合
    if (sample.efficiency_rating !== undefined && sample.modular !== undefined) {
      this.filterOptions.efficiency = [...new Set(this.originalData.map(item => item.efficiency_rating))].sort();
      this.filterOptions.modular = [0, 1]; // フルプラグイン対応
    }

    // ケースの場合
    if (sample.liquid_cooler !== undefined) {
      this.filterOptions.liquid = [0, 1]; // 水冷対応
    }
  }

  // フィルターセレクトボックスにオプションを追加
  populateFilterSelects() {
    // メーカーフィルター
    if (this.filterOptions.maker) {
      const makerSelect = document.getElementById('maker-filter');
      if (makerSelect) {
        this.filterOptions.maker.forEach(maker => {
          const option = document.createElement('option');
          option.value = maker;
          option.textContent = maker;
          makerSelect.appendChild(option);
        });
      }
    }

    // コア数フィルター (CPU)
    if (this.filterOptions.core) {
      const coreSelect = document.getElementById('core-filter');
      if (coreSelect) {
        this.filterOptions.core.forEach(core => {
          const option = document.createElement('option');
          option.value = core;
          option.textContent = `${core}コア`;
          coreSelect.appendChild(option);
        });
      }
    }

    // チップセットフィルター (GPU)
    if (this.filterOptions.chipset) {
      const chipsetSelect = document.getElementById('chipset-filter');
      if (chipsetSelect) {
        this.filterOptions.chipset.forEach(chipset => {
          const option = document.createElement('option');
          option.value = chipset;
          option.textContent = chipset;
          chipsetSelect.appendChild(option);
        });
      }
    }

    // VRAMフィルター (GPU)
    if (this.filterOptions.vram) {
      const vramSelect = document.getElementById('vram-filter');
      if (vramSelect) {
        this.filterOptions.vram.forEach(vram => {
          const option = document.createElement('option');
          option.value = vram;
          option.textContent = vram;
          vramSelect.appendChild(option);
        });
      }
    }

    // 容量フィルター (メモリ/ストレージ)
    if (this.filterOptions.capacity) {
      const capacitySelect = document.getElementById('capacity-filter');
      if (capacitySelect) {
        this.filterOptions.capacity.forEach(capacity => {
          const option = document.createElement('option');
          option.value = capacity;
          option.textContent = `${capacity}GB`;
          capacitySelect.appendChild(option);
        });
      }
    }

    // 速度フィルター (メモリ)
    if (this.filterOptions.speed) {
      const speedSelect = document.getElementById('speed-filter');
      if (speedSelect) {
        this.filterOptions.speed.forEach(speed => {
          const option = document.createElement('option');
          option.value = speed;
          option.textContent = `${speed}MHz`;
          speedSelect.appendChild(option);
        });
      }
    }

    // タイプフィルター (ストレージ/クーラー)
    if (this.filterOptions.type) {
      const typeSelect = document.getElementById('type-filter');
      if (typeSelect) {
        this.filterOptions.type.forEach(type => {
          const option = document.createElement('option');
          option.value = type;
          if (type === 'M2') {
            option.textContent = 'M.2';
          } else if (type === 'air') {
            option.textContent = '空冷';
          } else if (type === 'liquid') {
            option.textContent = '水冷';
          } else {
            option.textContent = type;
          }
          typeSelect.appendChild(option);
        });
      }
    }

    // ソケットフィルター (マザーボード)
    if (this.filterOptions.socket) {
      const socketSelect = document.getElementById('socket-filter');
      if (socketSelect) {
        this.filterOptions.socket.forEach(socket => {
          const option = document.createElement('option');
          option.value = socket;
          option.textContent = socket;
          socketSelect.appendChild(option);
        });
      }
    }

    // フォームファクターフィルター (マザーボード)
    if (this.filterOptions.formFactor) {
      const formFactorSelect = document.getElementById('form-factor-filter');
      if (formFactorSelect) {
        this.filterOptions.formFactor.forEach(factor => {
          const option = document.createElement('option');
          option.value = factor;
          option.textContent = factor;
          formFactorSelect.appendChild(option);
        });
      }
    }

    // 効率認証フィルター (電源)
    if (this.filterOptions.efficiency) {
      const efficiencySelect = document.getElementById('efficiency-filter');
      if (efficiencySelect) {
        this.filterOptions.efficiency.forEach(efficiency => {
          const option = document.createElement('option');
          option.value = efficiency;
          option.textContent = efficiency;
          efficiencySelect.appendChild(option);
        });
      }
    }

    // フルプラグインフィルター (電源)
    if (this.filterOptions.modular) {
      const modularSelect = document.getElementById('modular-filter');
      if (modularSelect) {
        const option1 = document.createElement('option');
        option1.value = '1';
        option1.textContent = '対応';
        modularSelect.appendChild(option1);

        const option0 = document.createElement('option');
        option0.value = '0';
        option0.textContent = '非対応';
        modularSelect.appendChild(option0);
      }
    }

    // 水冷対応フィルター (ケース)
    if (this.filterOptions.liquid) {
      const liquidSelect = document.getElementById('liquid-filter');
      if (liquidSelect) {
        const option1 = document.createElement('option');
        option1.value = '1';
        option1.textContent = '対応';
        liquidSelect.appendChild(option1);

        const option0 = document.createElement('option');
        option0.value = '0';
        option0.textContent = '非対応';
        liquidSelect.appendChild(option0);
      }
    }
  }

  // イベントリスナーを追加
  attachEventListeners() {
    if (!this.container) {
      console.error('Container not found, cannot attach event listeners');
      return;
    }
    
    const filterSelects = this.container.querySelectorAll('select[id$="-filter"]');
    
    filterSelects.forEach(select => {
      select.addEventListener('change', (e) => {
        const filterId = e.target.id.replace('-filter', '');
        this.filters[filterId] = e.target.value;
        this.applyFilters();
      });
    });

    // 検索ボックスがある場合
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.filters.search = e.target.value.toLowerCase();
        this.applyFilters();
      });
    }

    // フィルターリセットボタン
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
      resetButton.addEventListener('click', () => {
        this.resetFilters();
      });
    }
  }

  // フィルターを適用
  applyFilters() {
    this.filteredData = this.originalData.filter(item => {
      // メーカーフィルター
      if (this.filters.maker && item.maker !== this.filters.maker) {
        return false;
      }

      // コア数フィルター
      if (this.filters.core && item.core != this.filters.core) {
        return false;
      }

      // チップセットフィルター
      if (this.filters.chipset && (item.chipset_name || item.chipset_id) !== this.filters.chipset) {
        return false;
      }

      // VRAMフィルター
      if (this.filters.vram && item.vram !== this.filters.vram) {
        return false;
      }

      // 容量フィルター
      if (this.filters.capacity && item.capacity_gb != this.filters.capacity) {
        return false;
      }

      // 速度フィルター
      if (this.filters.speed && item.speed_mhz != this.filters.speed) {
        return false;
      }

      // タイプフィルター
      if (this.filters.type && (item.storage_type !== this.filters.type && item.cooler_type !== this.filters.type)) {
        return false;
      }

      // ソケットフィルター
      if (this.filters.socket && item.socket_type !== this.filters.socket) {
        return false;
      }

      // フォームファクターフィルター
      if (this.filters.formFactor && item.form_factor !== this.filters.formFactor) {
        return false;
      }

      // 効率認証フィルター
      if (this.filters.efficiency && item.efficiency_rating !== this.filters.efficiency) {
        return false;
      }

      // フルプラグインフィルター
      if (this.filters.modular && item.modular != this.filters.modular) {
        return false;
      }

      // 水冷対応フィルター
      if (this.filters.liquid && item.liquid_cooler != this.filters.liquid) {
        return false;
      }

      // 検索フィルター
      if (this.filters.search) {
        const searchTerm = this.filters.search;
        const searchableText = `${item.name} ${item.maker}`.toLowerCase();
        if (!searchableText.includes(searchTerm)) {
          return false;
        }
      }

      return true;
    });

    // フィルター結果を表示
    this.displayResults();
    this.updateResultCount();
  }

  // フィルター結果を表示
  displayResults() {
    // この関数は各ページで具体的な実装が必要
    if (window.renderFilteredProducts) {
      window.renderFilteredProducts(this.filteredData);
    }
  }

  // 結果件数を更新
  updateResultCount() {
    const countElement = document.getElementById('result-count');
    if (countElement) {
      countElement.textContent = `${this.filteredData.length}件の商品が見つかりました`;
    }
  }

  // フィルターをリセット
  resetFilters() {
    if (!this.container) {
      console.error('Container not found, cannot reset filters');
      return;
    }
    
    this.filters = {};
    this.filteredData = [...this.originalData];
    
    // セレクトボックスをリセット
    const filterSelects = this.container.querySelectorAll('select[id$="-filter"]');
    filterSelects.forEach(select => {
      select.value = '';
    });

    // 検索ボックスをリセット
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.value = '';
    }

    this.displayResults();
    this.updateResultCount();
  }

  // 現在のフィルター済みデータを取得
  getFilteredData() {
    return this.filteredData;
  }

  // フィルターを更新（新しいデータを設定）
  updateData(newData) {
    this.originalData = newData;
    this.filteredData = [...newData];
    this.extractFilterOptions();
    this.populateFilterSelects();
    this.applyFilters();
  }
}