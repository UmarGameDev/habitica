<template>
  <tr>
    <td colspan="3"
      v-if="!mixinData.inlineSettingMixin.modalVisible"
    >
      <div class="d-flex justify-content-between align-items-center">
        <h3
          v-once
          class="gray-50 mb-0"
        >
          {{ $t('yourPrivacyPreferences') }}
        </h3>
        <a
          class="edit-link"
          @click.prevent="openModal()"
        >
          {{ $t('edit') }}
        </a>
      </div>
    </td>
    <td colspan="3"
      v-if="mixinData.inlineSettingMixin.modalVisible"
    >
      <h3
        v-once
        class="purple-200 mb-0"
      >
        {{ $t('yourPrivacyPreferences') }}
      </h3>
      <p
        v-once
        class="gray-50 mb-4"
        v-html="$t('privacySettingsOverview') + ' ' + $t('learnMorePrivacy')"
      >
      </p>
      <div
        class="d-flex justify-content-center"
      >
        <div class="w-66">
          <div
            class="d-flex justify-content-between align-items-center mb-1"
          >
            <label class="settings-label w-50 mb-0">
              {{ $t('performanceAnalytics') }}
            </label>
            <toggle-switch
              class="mb-auto"
              v-model="user.preferences.analyticsConsent"
              @change="prefToggled()"
            />
          </div>
          <div class="mb-28p">
            <small class="gray-50">
              {{ $t('usedForSupport') }}
            </small>
          </div>
          <div
            class="d-flex justify-content-between align-items-center mb-1"
          >
            <label class="settings-label w-50 mb-0">
              {{ $t('strictlyNecessary') }}
            </label>
            <toggle-switch
              :checked="true"
              :disabled="true"
            />
          </div>
          <small class="gray-50">
            {{ $t('requiredToRun') }}
          </small>
          <save-cancel-buttons
            class="mb-4"
            :disable-save="!mixinData.inlineSettingMixin.sharedState.inlineSettingUnsavedValues"
            @saveClicked="finalize()"
            @cancelClicked="requestCloseModal()"
          />
        </div>
      </div>
    </td>
  </tr>
</template>

<style lang="scss" scoped>
  @import '@/assets/scss/colors.scss';

  button {
    width: fit-content;
  }

  small {
    line-height: 1.33;
  }

  .mb-28p {
    margin-bottom: 28px;
  }

  .popover-box {
    margin-top: 1px;
  }

  .w-66 {
    width: 66.7%;
  }
</style>

<script>
import SaveCancelButtons from '@/pages/settings/components/saveCancelButtons.vue';
import ToggleSwitch from '@/components/ui/toggleSwitch.vue';
import { GenericUserPreferencesMixin } from '@/pages/settings/components/genericUserPreferencesMixin';
import { InlineSettingMixin } from '../components/inlineSettingMixin';
import { mapState } from '@/libs/store';

export default {
  mixins: [
    GenericUserPreferencesMixin,
    InlineSettingMixin,
  ],
  components: {
    SaveCancelButtons,
    ToggleSwitch,
  },
  computed: {
    ...mapState({
      user: 'user.data',
    }),
  },
  methods: {
    finalize () {
      this.setUserPreference('analyticsConsent');
      this.mixinData.inlineSettingMixin.sharedState.inlineSettingUnsavedValues = false;
    },
    prefToggled () {
      const newVal = !this.mixinData.inlineSettingMixin.sharedState.inlineSettingUnsavedValues;
      this.mixinData.inlineSettingMixin.sharedState.inlineSettingUnsavedValues = newVal;
    },
    resetControls () {
      this.user.preferences.analyticsConsent = !this.user.preferences.analyticsConsent;
    },
  },
};
</script>
