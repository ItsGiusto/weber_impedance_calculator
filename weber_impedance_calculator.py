import enum
import matplotlib.pyplot as plt
import numpy as np

class ImpedanceSwitchSettings(enum.Enum):
	FOUR = 1
	EIGHT = 2
	SIXTEEN = 3

class MiniMassCalculator:
	DummyImpedance = 16.0
	ResistorToGround = 50.0
	@staticmethod
	def calcImpedance(impedanceSwitchSetting, attenuationPercent, speakerLoad):
		if impedanceSwitchSetting is ImpedanceSwitchSettings.FOUR:
			impedanceSwitchLoad = 8.0
			impedanceSwitchOn = True
		elif impedanceSwitchSetting is ImpedanceSwitchSettings.EIGHT:
			impedanceSwitchLoad = 16.0
			impedanceSwitchOn = True
		elif impedanceSwitchSetting is ImpedanceSwitchSettings.SIXTEEN:
			impedanceSwitchLoad = 0.0
			impedanceSwitchOn = False
		
		if impedanceSwitchOn:
			impedanceSwitchTerm = 1.0 / impedanceSwitchLoad
		else:
			impedanceSwitchTerm = 0.0
		
		attenuation = attenuationPercent / 100.0
		resistorParallelWithDummy = attenuation * MiniMassCalculator.ResistorToGround
		resistorLeftToGround = MiniMassCalculator.ResistorToGround - resistorParallelWithDummy
		
		if resistorParallelWithDummy == 0.0:
			totalDummyResistance = 0.0
		else:
			totalDummyResistance = 1.0 / ((1.0 / resistorParallelWithDummy) + (1.0 / MiniMassCalculator.DummyImpedance))
		
		if resistorLeftToGround == 0.0:
			resistanceToGround = 0.0
		else:
			resistanceToGround = 1.0 / ((1.0 / speakerLoad) + (1.0 / resistorLeftToGround))
		
		dummyPlusResistanceToGround = resistanceToGround + totalDummyResistance
		
		totalResistance = 1.0 / ((1.0 / dummyPlusResistanceToGround) + impedanceSwitchTerm)
		return totalResistance
	
		
	def plotImpedance(impedanceSwitchSetting, speakerLoad):
		attenuationPercent = np.linspace(0,100,101,endpoint=True)
		impedance = [MiniMassCalculator.calcImpedance(impedanceSwitchSetting, a, speakerLoad) for a in attenuationPercent]

		plt.plot(attenuationPercent, impedance)
		title = "%s\n Speaker Load = %s" % (impedanceSwitchSetting, speakerLoad)
		plt.grid(True)
		plt.title(title)
		
if __name__ == '__main__':

	plt.subplot(331)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.FOUR, 4.0)
	plt.subplot(332)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.FOUR, 8.0)
	plt.subplot(333)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.FOUR, 16.0)
	plt.subplot(334)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.EIGHT, 4.0)
	plt.subplot(335)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.EIGHT, 8.0)
	plt.subplot(336)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.EIGHT, 16.0)
	plt.subplot(337)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.SIXTEEN, 4.0)
	plt.subplot(338)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.SIXTEEN, 8.0)
	plt.subplot(339)
	MiniMassCalculator.plotImpedance(ImpedanceSwitchSettings.SIXTEEN, 16.0)
	
	plt.show()